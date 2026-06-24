from __future__ import annotations


def quote_style (quote : str) :
    """
    
    """
    return f"""
        <div style="text-align: center; padding-left:1rem; font-size: 24px; font-style: italic; margin-top: 20px;">
            "{quote}"
        </div>
    """



def author_style (author : str) :
    """
    
    """
    return f"""
        <div style="text-align: center; padding-left:1rem; font-size: 20px; font-weight: bold; margin-top: 10px;">
            - {author} 
        </div>
    """


