from __future__ import annotations

import datetime as dt
import os
import polars as pl

from typing import Optional, Dict, List, Tuple

from src.config.parameters import AEGIS_DISC_FUND_HV, AEGIS_IM_CTPY_COLUMNS, AEGIS_SIMM_CUTOFF_DATE
from src.config.paths import AEGIS_IM_CTPY_FILE, AEGIS_IM_CTPY_FUNDS_DIR_PATH
from src.utils.data_io import load_excel_to_dataframe
from src.utils.date import get_previous_bussiness_day, get_1m_bussiness_day, get_ytd_bussiness_day
from src.utils.formatter import str_to_date
from src.utils.logger import log


def _read_all_history (

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    Read a dated history file and apply the common cutoff/requested date filter.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    filename = AEGIS_IM_CTPY_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_CTPY_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    columns = list(schema_overrides.keys()) if schema_overrides is not None else None
    dir_abs_path = paths_by_fund.get(fund, None) if paths_by_fund is not None else None

    if filename is None or dir_abs_path is None :
        return None, None

    file_abs_path = os.path.join(dir_abs_path, filename)

    if not os.path.exists(file_abs_path) :
        return _empty_history_dataframe(schema_overrides), None

    try :
        dataframe, md5 = load_excel_to_dataframe(file_abs_path, specific_cols=columns, schema_overrides=schema_overrides)

    except Exception as e :

        log(f"Error during Excel lecture: {e}")
        return None, None

    if dataframe is None :
        return None, None

    dataframe = (
        dataframe
        .filter((pl.col("Date") >= cutoff_date) & (pl.col("Date") <= date))
        .sort("Date")
    )

    return dataframe, md5


def _empty_history_dataframe (schema_overrides : Optional[Dict] = None) -> pl.DataFrame :
    """
    Build an empty history dataframe with the expected schema.
    """
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides

    return pl.DataFrame(schema=schema_overrides)


def _get_latest_available_date (

        dataframe : Optional[pl.DataFrame] = None,
        date : Optional[str | dt.datetime | dt.date] = None,
        date_column : str = "Date",

    ) -> Optional[dt.date] :
    """
    Return the latest available date <= the requested date.
    """
    if dataframe is None or dataframe.is_empty() :
        return None

    date = str_to_date(date)

    return (
        dataframe
        .filter(pl.col(date_column) <= date)
        .select(pl.col(date_column).max())
        .item()
    )


def _get_values_by_date (

        dataframe : Optional[pl.DataFrame] = None,
        date : Optional[str | dt.datetime | dt.date] = None,
        schema_overrides : Optional[Dict] = None,
        date_column : str = "Date",

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Return rows for the latest available date <= the requested date.
    """
    if dataframe is None :
        return None, None

    available_date = _get_latest_available_date(dataframe, date, date_column)

    if available_date is None :
        return _empty_history_dataframe(schema_overrides), None

    return dataframe.filter(pl.col(date_column) == available_date), available_date


def _get_changes_from_date (

        dataframe : Optional[pl.DataFrame] = None,
        date : Optional[str | dt.datetime | dt.date] = None,

        value_col : str = "Value",
        group_col : Optional[str] = "Metric",
        date_column : str = "Date",
        metric_name : Optional[str] = None,

        nav_value : Optional[float] = None,
        alias_map : Optional[Dict] = None,
        change_mode : str = "relative_pct",

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute current value and 1D/1M/YTD changes from a dated history dataframe.
    """
    date = str_to_date(date)

    if dataframe is None :
        log("No history dataframe available.")
        return None, None

    required_columns = [date_column, value_col]

    if group_col is not None :
        required_columns.append(group_col)

    missing = [column for column in required_columns if column not in dataframe.columns]

    if missing :
        log(f"Missing history columns: {missing}")
        return None, None

    history = _prepare_changes_history(dataframe, date_column, value_col, group_col, metric_name, alias_map)

    if history is None or history.is_empty() :
        log("No history available for changes.")
        return None, None

    real_date = _get_latest_available_date(history, date, date_column)

    if real_date is None :
        log("No data available before or at the requested date.")
        return None, None

    history = history.filter(pl.col(date_column) <= real_date).sort(["Metric", date_column])
    current_dataframe = history.filter(pl.col(date_column) == real_date)

    if current_dataframe.is_empty() :
        log("No current row available for the real date.")
        return None, real_date

    changes_dataframe = _build_changes_output(
        current_dataframe,
        history,
        real_date,
        date_column,
        nav_value,
        change_mode,
    )

    return changes_dataframe, real_date


def _prepare_changes_history (

        dataframe : Optional[pl.DataFrame] = None,
        date_column : str = "Date",
        value_col : str = "Value",
        group_col : Optional[str] = "Metric",
        metric_name : Optional[str] = None,
        alias_map : Optional[Dict] = None,

    ) -> Optional[pl.DataFrame] :
    """
    Normalize a history dataframe to Date | Metric | Value.
    """
    if dataframe is None :
        return None

    alias_map = _clean_alias_map(alias_map)

    if alias_map and group_col is not None :
        dataframe = dataframe.with_columns(pl.col(group_col).replace(alias_map))

    dataframe = dataframe.with_columns(
        pl.col(date_column).cast(pl.Date).alias(date_column),
        pl.col(value_col).cast(pl.Float64, strict=False).alias(value_col),
    )

    if group_col is None :

        return (
            dataframe
            .drop_nulls(subset=[date_column, value_col])
            .group_by(date_column)
            .agg(pl.col(value_col).sum().alias("Value"))
            .with_columns(pl.lit("Value" if metric_name is None else metric_name).alias("Metric"))
            .select([date_column, "Metric", "Value"])
        )

    return (
        dataframe
        .drop_nulls(subset=[date_column, group_col, value_col])
        .group_by([date_column, group_col])
        .agg(pl.col(value_col).sum().alias("Value"))
        .rename({group_col : "Metric"})
        .select([date_column, "Metric", "Value"])
    )


def _build_changes_output (

        current_dataframe : Optional[pl.DataFrame] = None,
        history : Optional[pl.DataFrame] = None,
        real_date : Optional[dt.date] = None,
        date_column : str = "Date",
        nav_value : Optional[float] = None,
        change_mode : str = "relative_pct",

    ) -> Optional[pl.DataFrame] :
    """
    Build final changes output.
    """
    if current_dataframe is None or history is None :
        return None

    metrics = current_dataframe.get_column("Metric").unique().sort().to_list()
    reference_dataframe = _build_reference_dates_dataframe(real_date, metrics)
    matched = _match_reference_dates(reference_dataframe, history, date_column)

    if matched.is_empty() :
        return None

    matched_rows = {
        (row["Metric"], row["Label"]) : row
        for row in matched.to_dicts()
    }

    rows = []

    for row in current_dataframe.sort("Metric").to_dicts() :

        metric = row["Metric"]
        current_value = row["Value"]

        out = {
            "Metric" : metric,
            "Real Date" : real_date,
            "Current Value" : current_value,
        }

        if nav_value is not None and nav_value != 0 :
            out["Current Value / NAV (%)"] = (current_value / nav_value) * 100

        for label in _get_reference_labels(reference_dataframe) :

            matched_row = matched_rows.get((metric, label), {})
            historical_value = matched_row.get("Value")
            out[label] = _compute_change(current_value, historical_value, nav_value, change_mode)

        rows.append(out)

    if len(rows) == 0 :
        return None

    return pl.DataFrame(rows)


def _build_reference_dates_dataframe (

        date : Optional[str | dt.date | dt.datetime] = None,
        metrics : Optional[List[str]] = None,

    ) -> pl.DataFrame :
    """
    Build reference dates used to compute changes.
    """
    date = str_to_date(date)
    metrics = ["Value"] if metrics is None else metrics

    reference_dates = {
        "1D Change (%)" : get_previous_bussiness_day(date),
        "1M Change (%)" : get_1m_bussiness_day(date),
        "YTD Change (%)" : get_ytd_bussiness_day(date),
    }

    rows = [
        {
            "Metric" : metric,
            "Label" : label,
            "Check Date" : check_date,
            "Display Order" : index,
        }
        for metric in metrics
        for index, (label, check_date) in enumerate(reference_dates.items())
    ]

    return (
        pl.DataFrame(rows)
        .with_columns(pl.col("Check Date").cast(pl.Date))
        .sort(["Metric", "Display Order"])
    )


def _match_reference_dates (

        reference_dataframe : Optional[pl.DataFrame] = None,
        history : Optional[pl.DataFrame] = None,
        date_column : str = "Date",

    ) -> pl.DataFrame :
    """
    Match each metric reference date to the latest historical row before it.
    """
    if reference_dataframe is None or history is None :
        return pl.DataFrame()

    matched_dataframes = []
    metrics = reference_dataframe.get_column("Metric").unique().sort().to_list()

    for metric in metrics :

        reference_metric_dataframe = (
            reference_dataframe
            .filter(pl.col("Metric") == metric)
            .sort("Check Date")
        )

        history_metric_dataframe = (
            history
            .filter(pl.col("Metric") == metric)
            .sort(date_column)
        )

        if history_metric_dataframe.is_empty() :
            continue

        matched_dataframes.append(
            reference_metric_dataframe.join_asof(
                history_metric_dataframe,
                left_on="Check Date",
                right_on=date_column,
                strategy="backward",
            )
        )

    if len(matched_dataframes) == 0 :
        return pl.DataFrame()

    return pl.concat(matched_dataframes)


def _get_reference_labels (

        reference_dataframe : Optional[pl.DataFrame] = None,

    ) -> List[str] :
    """
    Return reference labels in display order.
    """
    if reference_dataframe is None or reference_dataframe.is_empty() :
        return []

    labels_dataframe = (
        reference_dataframe
        .select(["Label", "Display Order"])
        .unique(subset=["Label"], maintain_order=True)
        .sort("Display Order")
    )

    return labels_dataframe.get_column("Label").to_list()


def _compute_change (

        current_value : Optional[float | int] = None,
        historical_value : Optional[float | int] = None,
        nav_value : Optional[float | int] = None,
        change_mode : str = "relative_pct",

    ) -> Optional[float] :
    """
    Compute a change using the requested mode.
    """
    if change_mode == "nav_pct_point" :
        return _compute_nav_pct_point_change(current_value, historical_value, nav_value)

    return _compute_relative_pct_change(current_value, historical_value)


def _compute_relative_pct_change (

        current_value : Optional[float | int] = None,
        historical_value : Optional[float | int] = None,

    ) -> Optional[float] :
    """
    Compute percentage change between current and historical value.
    """
    if current_value is None :
        return None

    if historical_value is None or historical_value == 0 :
        return None

    return ((current_value - historical_value) / historical_value) * 100


def _compute_nav_pct_point_change (

        current_value : Optional[float | int] = None,
        historical_value : Optional[float | int] = None,
        nav_value : Optional[float | int] = None,

    ) -> Optional[float] :
    """
    Compute percentage-point change of value / NAV.
    """
    if current_value is None or historical_value is None :
        return None

    if nav_value is None or nav_value == 0 :
        return None

    current_pct = (current_value / nav_value) * 100
    historical_pct = (historical_value / nav_value) * 100

    return current_pct - historical_pct


def _clean_alias_map (alias_map : Optional[Dict] = None) -> Optional[Dict] :
    """
    Drop empty alias entries coming from optional environment variables.
    """
    if not alias_map :
        return None

    clean_map = {key : value for key, value in alias_map.items() if key is not None and value is not None}

    return clean_map or None
