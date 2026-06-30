from __future__ import annotations

import os
import polars as pl
import datetime as dt

from typing import Optional, Dict, List, Tuple

from src.utils.logger import log
from src.config.parameters import (
    AEGIS_DISC_FUND_HV, AEGIS_IM_CTPY_COLUMNS, AEGIS_IM_ICE_COLUMNS,
    AEGIS_SIMM_CUTOFF_DATE
)
from src.config.paths import (
    AEGIS_IM_CTPY_FILE, AEGIS_IM_ICE_FILE,
    AEGIS_IM_CTPY_FUNDS_DIR_PATH, AEGIS_IM_ICE_FUNDS_DIR_PATH
)
from src.utils.data_io import load_excel_to_dataframe
from src.utils.formatter import str_to_date
from src.utils.date import (
    get_previous_bussiness_day, get_1m_bussiness_day, get_ytd_bussiness_day
)


def get_im_ctpy_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str ] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,
        
        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None
        
    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    filename = AEGIS_IM_CTPY_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_CTPY_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    dataframe, md5 = _read_im_all_history(date, fund, filename, paths_by_fund, schema_overrides, cutoff_date)

    return dataframe, md5


def get_im_ice_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str ] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,
        
        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None
        
    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    filename = AEGIS_IM_ICE_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_ICE_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    
    schema_overrides = AEGIS_IM_ICE_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)
    
    dataframe, md5 = _read_im_all_history(date, fund, filename, paths_by_fund, schema_overrides, cutoff_date)
    
    return dataframe, md5


def get_im_ctpy_values_by_date (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        schema_overrides : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str], Optional[dt.date]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund) if dataframe is None else (dataframe, md5)

    if dataframe is None :
        return None, None, None
    
    available_date = _get_available_date(dataframe, date)

    if available_date is None :

        schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
        return _empty_simm_history_dataframe(schema_overrides), None, None
    
    dataframe = dataframe.filter(pl.col("Date") == available_date)

    return dataframe, md5, available_date


def get_im_ice_values_by_date (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        schema_overrides : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str], Optional[dt.date]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ice_all_history(date, fund) if dataframe is None else (dataframe, md5)

    if dataframe is None :
        return None, None, None
    
    available_date = _get_available_date(dataframe, date)

    if available_date is None :

        schema_overrides = AEGIS_IM_ICE_COLUMNS if schema_overrides is None else schema_overrides
        return _empty_simm_history_dataframe(schema_overrides), None, None
    
    dataframe = dataframe.filter(pl.col("Date") == available_date)

    return dataframe, md5, available_date


def get_simm_nav_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute total ICE IM changes used for the SIMM/NAV control.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ice_all_history(date, fund) if dataframe is None else (dataframe, md5)
    dataframe, md5 = get_simm_changes_from_date(

        dataframe=dataframe,
        md5=md5,
        date=date,
        fund=fund,
        value_col="IM",
        group_col=None,
        metric_name="SIMM",
        nav_value=nav_value,
        change_mode="nav_pct_point",
    
    )

    return dataframe, md5


def get_im_ctpy_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute IM changes from counterparty data history.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund) if dataframe is None else (dataframe, md5)
    dataframe, md5 = get_simm_changes_from_date(

        dataframe=dataframe,
        md5=md5,
        date=date,
        fund=fund,
        value_col="IM",
        group_col="Bank",
        nav_value=nav_value,
    
    )

    return dataframe, md5


def get_im_ice_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,
        rename_map : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute IM changes from ICE history.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ice_all_history(date, fund) if dataframe is None else (dataframe, md5)
    dataframe, md5 = get_simm_changes_from_date(

        dataframe=dataframe,
        md5=md5,
        date=date,
        fund=fund,
        value_col="IM",
        group_col="Counterparty",
        nav_value=nav_value,
        alias_map=rename_map,
    
    )

    return dataframe, md5


def get_vm_ctpy_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute VM changes from counterparty data history.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund) if dataframe is None else (dataframe, md5)

    return get_simm_changes_from_date(
        dataframe=dataframe,
        md5=md5,
        date=date,
        fund=fund,
        value_col="VM",
        group_col="Bank",
        nav_value=nav_value,
    )


def get_vm_ice_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,
        rename_map : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute VM changes from ICE history.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ice_all_history(date, fund) if dataframe is None else (dataframe, md5)

    return get_simm_changes_from_date(
        dataframe=dataframe,
        md5=md5,
        date=date,
        fund=fund,
        value_col="MV",
        group_col="Counterparty",
        nav_value=nav_value,
        alias_map=rename_map,
    )


def get_simm_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        value_col : str = "IM",
        group_col : Optional[str] = "Bank",
        date_column : str = "Date",
        metric_name : Optional[str] = None,

        nav_value : Optional[float] = None,
        alias_map : Optional[Dict] = None,
        change_mode : str = "relative_pct",

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute current value and 1D/1M/YTD percentage changes from SIMM history.

    The current date used in calculations is the latest available date <= the
    requested date. Reference dates are then computed from that real date.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    if dataframe is None :

        log("No SIMM history dataframe available.")
        return None, None

    missing = [column for column in [date_column, value_col, group_col] if column is not None and column not in dataframe.columns]

    if missing :

        log(f"Missing SIMM columns: {missing}")
        return None, None

    history = _prepare_simm_changes_history(dataframe, date_column, value_col, group_col, metric_name, alias_map)

    if history is None or history.is_empty() :

        log("No SIMM history available for changes.")
        return None, None

    real_date = _get_available_date(history, date, date_column)

    if real_date is None :

        log("No SIMM data available before or at the requested date.")
        return None, None

    history = history.filter(pl.col(date_column) <= real_date).sort(["Metric", date_column])
    current_dataframe = history.filter(pl.col(date_column) == real_date)

    if current_dataframe.is_empty() :

        log("No current SIMM row available for the real date.")
        return None, real_date

    changes_dataframe = _build_simm_changes_output(
        current_dataframe,
        history,
        real_date,
        date_column,
        nav_value,
        change_mode,
    )

    return changes_dataframe, real_date


# --------------------- Auxiliar functions ---------------------

def _read_im_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str ] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,
        
        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None
        
    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    filename = AEGIS_IM_CTPY_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_CTPY_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    columns = list(schema_overrides.keys()) if schema_overrides is not None else None

    dir_abs_path = paths_by_fund.get(fund, None)
    
    if filename is None or dir_abs_path is None :
        return None, None
    
    file_abs_path = os.path.join(dir_abs_path, filename)
    if not os.path.exists(file_abs_path) :
        return _empty_simm_history_dataframe(schema_overrides), None

    try :
        dataframe, md5 = load_excel_to_dataframe(file_abs_path, specific_cols=columns, schema_overrides=schema_overrides) 

    except Exception as e :

        log(f"Error during Excel lecture: {e}")
        return None, None
    
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    dataframe = dataframe.filter((pl.col("Date") >= (cutoff_date)) & (pl.col("Date") <= (date)))
    dataframe = dataframe.sort("Date")

    return dataframe, md5


def _empty_simm_history_dataframe (schema_overrides : Optional[Dict] = None) -> pl.DataFrame :
    """
    Build an empty SIMM history dataframe with the expected schema.
    """
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    dataframe = pl.DataFrame(schema=schema_overrides)

    return dataframe


def _get_available_date (
        
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

    available_date = (
        dataframe
        .filter(pl.col(date_column) <= date)
        .select(pl.col(date_column).max())
        .item()
    )

    return available_date


def _prepare_simm_changes_history (
        
        dataframe : Optional[pl.DataFrame] = None,
        date_column : str = "Date",
        value_col : str = "IM",
        group_col : Optional[str] = "Bank",
        metric_name : Optional[str] = None,
        alias_map : Optional[Dict] = None,

    ) -> Optional[pl.DataFrame] :
    """
    Normalize SIMM history to Date | Metric | Value.
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

        dataframe = (
            dataframe
            .drop_nulls(subset=[date_column, value_col])
            .group_by(date_column)
            .agg(pl.col(value_col).sum().alias("Value"))
            .with_columns(pl.lit("SIMM" if metric_name is None else metric_name).alias("Metric"))
            .select([date_column, "Metric", "Value"])
        )

        return dataframe

    dataframe = (
        dataframe
        .drop_nulls(subset=[date_column, group_col, value_col])
        .group_by([date_column, group_col])
        .agg(pl.col(value_col).sum().alias("Value"))
        .rename({group_col : "Metric"})
        .select([date_column, "Metric", "Value"])
    )

    return dataframe


def _build_simm_changes_output (
        
        current_dataframe : Optional[pl.DataFrame] = None,
        history : Optional[pl.DataFrame] = None,
        real_date : Optional[dt.date] = None,
        date_column : str = "Date",
        nav_value : Optional[float] = None,
        change_mode : str = "relative_pct",

    ) -> Optional[pl.DataFrame] :
    """
    Build final output:

    Metric | Real Date | Current Value | Current Value / NAV (%) | 1D Change (%) | ...
    """
    if current_dataframe is None or history is None :
        return None

    metrics = current_dataframe.get_column("Metric").unique().sort().to_list()
    reference_dataframe = _build_simm_reference_dates_dataframe(real_date, metrics)

    matched = _match_simm_reference_dates(reference_dataframe, history, date_column)

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

        for label in _get_simm_reference_labels(reference_dataframe) :

            matched_row = matched_rows.get((metric, label), {})
            historical_value = matched_row.get("Value")
            out[label] = _compute_simm_change(current_value, historical_value, nav_value, change_mode)

        rows.append(out)

    if len(rows) == 0 :
        return None

    return pl.DataFrame(rows)


def _build_simm_reference_dates_dataframe (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        metrics : Optional[List[str]] = None,

    ) -> pl.DataFrame :
    """
    Build reference dates used to compute SIMM changes.
    """
    date = str_to_date(date)
    metrics = ["SIMM"] if metrics is None else metrics

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

    reference_dataframe = (
        pl.DataFrame(rows)
        .with_columns(pl.col("Check Date").cast(pl.Date))
        .sort(["Metric", "Display Order"])
    )

    return reference_dataframe


def _match_simm_reference_dates (
        
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


def _get_simm_reference_labels (
        
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


def _compute_change_pct (
        
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

    change_pct = ((current_value - historical_value) / historical_value) * 100

    return change_pct


def _compute_simm_change (
        
        current_value : Optional[float | int] = None,
        historical_value : Optional[float | int] = None,
        nav_value : Optional[float | int] = None,
        change_mode : str = "relative_pct",

    ) -> Optional[float] :
    """
    Compute SIMM change using the requested change mode.
    """
    if change_mode == "nav_pct_point" :
        return _compute_nav_pct_point_change(current_value, historical_value, nav_value)

    return _compute_change_pct(current_value, historical_value)


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
