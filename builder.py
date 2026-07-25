import pandas as pd

def get_best_build(df, budget, category):
    """
    專門處理配單邏輯的獨立函式
    """
    # 執行篩選
    mask = (df['Budget'] <= budget) & (df['Category'] == category)
    filtered_df = df[mask]
    
    if filtered_df.empty:
        return None
    
    # 回傳符合條件的第一筆最佳解
    return filtered_df.iloc[0]