from __future__ import annotations

import html
from typing import Any, Optional
from collections.abc import Callable, Iterable, Sequence

import streamlit as st
import streamlit.components.v1 as components


ChatChannel = tuple[str, str]
ChatMessage = tuple[str, str, Optional[str]]
LoadMessages = Callable[[str], Iterable[ChatMessage | Sequence[Any] | dict[str, Any]]]
SendMessage = Callable[[str, str, str], None]


DEFAULT_CHANNELS: tuple[ChatChannel, ...] = (
    ("Hedge Fund Chat", "HF_chat"),
    ("Financial Advisory Chat", "advisory_chat"),
    ("Company Chat", "full_chat"),
    ("Technology Chat", "tech_chat"),
    ("Compliance Chat", "compliance_chat"),
)


def chat (
        
        current_user : str,
        
        load_messages : LoadMessages,
        send_message : SendMessage,
        channels : Sequence[ChatChannel | dict[str, str]] = DEFAULT_CHANNELS,
        
        title : Optional[str] = "Chat",
        subtitle : Optional[str] = None,
        
        key : str = "chat",
        height : int = 550,
        empty_message : str = "No messages yet.",

    ) -> Optional[str] :
    """
    
    """
    channel_options = normalize_channels(channels)

    if not channel_options :
    
        st.warning("No chat channels configured.")
        return None

    render_chat_header(title=title, subtitle=subtitle)
    
    selected_channel = select_chat_channel(
        
        channels=channel_options,
        key=key,
    
    )
    
    messages = get_channel_messages(
        
        channel=selected_channel,
        load_messages=load_messages,
    
    )

    render_chat_history(
    
        messages=messages,
        current_user=current_user,
        height=height,
        empty_message=empty_message,
    
    )
    
    render_refresh_button(key=key)

    render_message_form(
        
        channel=selected_channel,
        current_user=current_user,
        send_message=send_message,
        key=key,
    
    )

    return selected_channel


def render_chat_header (
        
        title : Optional[str],
        subtitle : Optional[str] = None,
    
    ) -> None :
    """
    
    """
    if title :
        st.subheader(title)
    
    if subtitle :
        st.caption(subtitle)

    return None


def select_chat_channel (
        
        channels : Sequence[ChatChannel],
        key : str,
    
    ) -> str :
    """
    
    """
    selected_label = st.selectbox(
        
        "Choose a chat",
        options=[label for label, _ in channels],
        key=f"{key}_channel_selector",
    
    )

    return get_channel_value(
        
        channels=channels,
        selected_label=str(selected_label),
    
    )


def get_channel_value (
        
        channels : Sequence[ChatChannel],
        selected_label : str,
    
    ) -> str :
    """
    
    """
    for label, value in channels :

        if label == selected_label :
            return value
    
    return channels[0][1]


def get_channel_messages (
        
        channel : str,
        load_messages : LoadMessages,
    
    ) -> list[ChatMessage] :
    """
    
    """
    return [
        
        normalize_message(message)
        for message in load_messages(channel)
    
    ]


def render_chat_history (
        
        messages : Iterable[ChatMessage],
        current_user : str,
        height : int,
        empty_message : str,
    
    ) -> None :
    """
    
    """
    components.html(
        
        get_chat_html(
            
            messages=messages,
            current_user=current_user,
            empty_message=empty_message,
        
        ),
        height=height,
        scrolling=False,
    
    )

    return None


def render_refresh_button (
        
        key : str,
    
    ) -> None :
    """
    
    """
    refresh_col, _ = st.columns([1, 4])
    
    with refresh_col :
    
        if st.button("Refresh", key=f"{key}_refresh_button", type="secondary") :
            st.rerun()

    return None


def render_message_form (
        
        channel : str,
        current_user : str,
        send_message : SendMessage,
        key : str,
    
    ) -> None :
    """
    
    """
    with st.form(key=f"{key}_form", clear_on_submit=True) :
    
        user_input = st.text_area("Type your message:", key=f"{key}_message_input")
        submitted = st.form_submit_button("Send", type="primary")

    if submitted and user_input.strip() :
    
        send_message(channel, current_user, user_input.strip())
        st.rerun()

    return None


def get_chat_html (
        
        messages : Iterable[ChatMessage],
        current_user : str,
        empty_message : str = "No messages yet.",
    
    ) -> str :
    """
    
    """
    message_html = build_messages_html(
        
        messages=messages,
        current_user=current_user,
        empty_message=empty_message,
    
    )

    return f"""
    {get_chat_style()}
    <div class="chat-container" id="chat-box">
        {message_html}
    </div>
    {get_chat_script()}
    """


def build_messages_html (
        
        messages : Iterable[ChatMessage],
        current_user : str,
        empty_message : str,
    
    ) -> str :
    """
    
    """
    rendered_messages = [
        
        build_message_html(
            
            message=message,
            current_user=current_user,
        
        )
        for message in messages
    
    ]
    
    if not rendered_messages :
        return f'<p class="chat-empty">{html.escape(empty_message)}</p>'
    
    return "".join(rendered_messages)


def build_message_html (
        
        message : ChatMessage,
        current_user : str,
    
    ) -> str :
    """
    
    """
    author, content, timestamp = message
    
    message_class = "user-message" if author == current_user else "other-message"
    
    safe_author = html.escape(author)
    safe_content = html.escape(content).replace("\n", "<br>")
    safe_timestamp = html.escape(timestamp or "")

    return f"""
    <div class="chat-message {message_class}" data-timestamp="{safe_timestamp}">
        <b>{safe_author}</b>
        <span>{safe_content}</span>
    </div>
    """


def get_chat_style () -> str :
    """
    
    """
    return """
    <style>
    .chat-container {
        background-color: #f7f7f7;
        padding: 16px;
        border-radius: 8px;
        height: calc(100vh - 8px);
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        scroll-behavior: smooth;
        border: 1px solid #d7dce5;
        box-sizing: border-box;
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .chat-message {
        padding: 12px 14px;
        border-radius: 8px;
        margin: 8px 0;
        max-width: 85%;
        font-size: 15px;
        line-height: 1.4;
        overflow-wrap: anywhere;
        position: relative;
    }

    .chat-message b {
        display: block;
        font-size: 13px;
        margin-bottom: 4px;
        color: rgba(255, 255, 255, 0.9);
    }

    .chat-message span {
        white-space: normal;
    }

    .user-message {
        background-color: #061237;
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 2px;
    }

    .other-message {
        background-color: #3972e5;
        color: white;
        align-self: flex-start;
        border-bottom-left-radius: 2px;
    }

    .chat-message[data-timestamp]:not([data-timestamp=""]):hover::after {
        content: attr(data-timestamp);
        position: absolute;
        bottom: -24px;
        left: 8px;
        z-index: 1;
        font-size: 12px;
        color: #465166;
        background: #eef2f7;
        padding: 4px 6px;
        border-radius: 6px;
        white-space: nowrap;
        border: 1px solid #d7dce5;
    }

    .chat-empty {
        color: #667085;
        margin: auto;
        font-size: 14px;
    }
    </style>
    """


def get_chat_script () -> str :
    """
    
    """
    return """
    <script>
    function scrollToBottom() {
        const chatBox = document.getElementById("chat-box");
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
    window.addEventListener("load", scrollToBottom);
    setTimeout(scrollToBottom, 100);
    </script>
    """


def normalize_channels (
        
        channels : Sequence[ChatChannel | dict[str, str]],
    
    ) -> tuple[ChatChannel, ...] :
    """
    
    """
    return tuple(
        
        normalize_channel(channel)
        for channel in channels
    
    )


def normalize_channel (
        
        channel : ChatChannel | dict[str, str],
    
    ) -> ChatChannel :
    """
    
    """
    if isinstance(channel, dict) :
    
        label = channel.get("label") or channel.get("name") or ""
        value = channel.get("value") or channel.get("id") or label
        
        return str(label), str(value)

    label, value = channel
    
    return str(label), str(value)


def normalize_message (
        
        message : ChatMessage | Sequence[Any] | dict[str, Any],
    
    ) -> ChatMessage :
    """
    
    """
    if isinstance(message, dict) :
    
        return (
            
            str(message.get("author") or message.get("user") or ""),
            str(message.get("content") or message.get("message") or ""),
            optional_str(message.get("timestamp")),
        
        )

    author, content, *rest = message
    timestamp = rest[0] if rest else None
    
    return str(author), str(content), optional_str(timestamp)


def optional_str (
        
        value : Any,
    
    ) -> Optional[str] :
    """
    
    """
    if value is None :
        return None
    
    return str(value)
