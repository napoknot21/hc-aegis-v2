from __future__ import annotations

import os
import msal
import jwt
import json
import requests
import datetime as dt

from typing import Dict, List, Optional, Any, Tuple, Union

from src.utils.formater import date_to_str, convert_bytes_64
from src.config.parameters import (

    AEGIS_MSAL_CLIENT_SECRET_VALUE, AEGIS_MSAL_SCOPES, AEGIS_MSAL_CLIENT_ID, AEGIS_MSAL_TENANT_ID,
    AEGIS_MSAL_EMAIL_SENDER_MAIL, AEGIS_MSAL_EMAIL_RECIPIENT_MAIL, AEGIS_MSAL_EMAIL_BREACH_LOG_SUBJECT,
    AEGIS_MSAL_EMAIL_BREACH_LOG_CONTENT, AEGIS_MSAL_GRAPH_BASE, AEGIS_MSAL_AUTHORITY

)


def get_token (
        
        scopes : Optional[List] = None,
        app_id : Optional[str] =  None,
        authority : Optional[str] = None,
        secret :  Optional[str] = None
    
    ) -> Optional[str] :
    """
    Function get token from the applcation 
    """
    scopes = AEGIS_MSAL_SCOPES if scopes is None else scopes

    app_id = AEGIS_MSAL_CLIENT_ID if app_id is None else app_id
    authority = AEGIS_MSAL_AUTHORITY if authority is None else authority
    secret = AEGIS_MSAL_CLIENT_SECRET_VALUE if secret is None else secret
    
    app = msal.ConfidentialClientApplication(

        client_id=app_id,
        authority=authority,
        client_credential=secret

    )

    result = app.acquire_token_for_client(

        scopes=scopes

    )

        
    if "access_token" in result :

        print("\n[+] Token acquired successfully")
        print(result["access_token"][:30] + "...")  # Print just token first 30 letters
    
    else :

        print("\n[-] Failed to acquire token\n")
        print(result.get("error_description"))

    return result.get("access_token", None)


def decode_token (token : str) -> List[Dict[str, Any]] :

    if token is None :
        return None
    
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    print("\n[*] Token claims :")
    print("\t[*] roles: ", decoded.get("roles"))
    print("\t[*] App Id:", decoded.get("appid"))
    
    return decoded


def send_email (
        
        token : Optional[str] = None,
        
        sender : Optional[str] = None,
        recipients : Optional[List[str]] = None,
        
        subject : Optional[str] = None,
        content : Optional[str] = None,
        
        file_abs_path : Optional[List[str]] = None,
        graph_base : Optional[str] = None

    ) :
    """
    Send a plain-text email through Microsoft Graph.

    If no token is provided, the function obtains one with `get_token`.
    Sender, recipients, subject, and Graph base URL default to the values from
    `src.config`. Optional file paths are attached after base64 encoding.
    """
    token = get_token() if token is None else token

    if token is None :

        print("[-] No token available. Cannot send email.")
        return False

    headers = {

        "Authorization" : f"Bearer {token}",
        "Content-Type" : "application/json"

    }

    sender = AEGIS_MSAL_EMAIL_SENDER_MAIL if sender is None else sender
    recipients = AEGIS_MSAL_EMAIL_RECIPIENT_MAIL if recipients is None else recipients
    
    subject = AEGIS_MSAL_EMAIL_BREACH_LOG_SUBJECT if subject is None else subject
    content = AEGIS_MSAL_EMAIL_BREACH_LOG_CONTENT if content is None else content

    graph_base = AEGIS_MSAL_GRAPH_BASE if graph_base is None else graph_base
    recipients = [recipients] if isinstance(recipients, str) else recipients

    if recipients is None or len(recipients) == 0 :

        print("[-] No recipients provided. Cannot send email.")
        return False

    url = f"{graph_base}/users/{sender}/sendMail"

    payload = {

        "message" : {

            "subject" : subject,
            "body" : {

                "contentType" : "text",
                "content" : content

            },
            "toRecipients" : [

                {
                    "emailAddress" : {
                        "address" : recipient
                    }
                }
                for recipient in recipients

            ]

        },
        "saveToSentItems" : "true"
    }


    if file_abs_path is not None :
    
        if isinstance(file_abs_path, list) :
            files = file_abs_path

        else :
            files = [file_abs_path]

        for file_path in files :

            if os.path.exists(file_path) :

                base_name = os.path.basename(file_path)
                bytes_file = convert_bytes_64(file_path)

                attachment = [

                    {
                        "@odata.type" : "#microsoft.graph.fileAttachment",
                        "name" : base_name,
                        "contentType" : "text/plain",
                        "contentBytes" : bytes_file,
                    }

                ]

                payload["message"]["attachments"] = attachment

            else :
                print(f"[-] File {file_path} does not exist. Sending without attachment")

    try :

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(response.text)

    except Exception as e :

        print("\n[-] error while sending email")
        return False
    
    print("[+] Email send")
    return True

