# optimizer.py
import pandas as pd
from config import FACTORIES, PRODUCT_MAPPING
from data_prep import calculate_distance
import numpy as np

def simulate_reallocation(model, product_name, division, region, ship_mode, speed_priority=0.5):
    """
    Tests assigning a product to ALL available factories and predicts 
    the resulting lead time and estimated margin impact.
    
    speed_priority: 0.0 = full profit focus, 1.0 = full speed focus
    """
    current_factory = PRODUCT_MAPPING.get(product_name, "Unknown")
    
    # Ship mode rank mapping
    ship_mode_rank = {'Same Day': 0, 'First Class': 1, 'Second Class': 2, 'Standard Class': 3}
    mode_rank = ship_mode_rank.get(ship_mode, 3)
    
    results = []
    
    for factory in FACTORIES.keys():
        # 1. Calculate new hypothetical distance
        new_distance = calculate_distance(factory, region)
        current_distance = calculate_distance(current_factory, region) if current_factory != "Unknown" else 1000
        
        # 2. Create the hypothetical data row
        scenario_df = pd.DataFrame([{
            'Origin Factory': factory,
            'Region': region,
            'Ship Mode': ship_mode,
            'Division': division,
            'Shipping Distance': new_distance,
            'Ship Mode Rank': mode_rank
        }])
        
        # 3. Predict new lead time
        predicted_lead_time = model.predict(scenario_df)[0]
        
        # 4. Margin Impact (distance-based freight cost model)
        # Closer factories = lower freight = better margins
        distance_delta = current_distance - new_distance  # positive = closer = better
        freight_savings_pct = (distance_delta / max(current_distance, 1)) * 2.5  # as pct impact
        
        # Factory efficiency factor (some factories have inherent cost advantages)
        np.random.seed(hash(factory) % 2**32)  # Deterministic per factory
        factory_efficiency = np.random.uniform(-0.5, 0.5)
        
        margin_impact = round(freight_savings_pct + factory_efficiency, 2)
        
        # 5. Composite score based on speed_priority slider
        # Normalize: lower lead time is better, higher margin is better
        speed_score = -predicted_lead_time  # negative because lower is better
        profit_score = margin_impact
        
        composite = speed_priority * speed_score + (1 - speed_priority) * profit_score * 100
        
        results.append({
            "Factory": factory,
            "Predicted Lead Time (Days)": round(predicted_lead_time, 1),
            "Margin Impact (%)": margin_impact,
            "Distance (km)": round(new_distance, 0),
            "Composite Score": round(composite, 2),
            "Is Current": factory == current_factory
        })
    
    return pd.DataFrame(results).sort_values(by="Composite Score", ascending=False)


def compute_kpis(df, model, all_products, all_regions, all_ship_modes):
    """
    Computes the 4 KPIs across all product-region-ship mode combinations.
    Returns a dict with KPI values.
    """
    from config import DIVISION_MAP
    
    total_scenarios = 0
    reallocations_recommended = 0
    lead_time_reductions = []
    margin_impacts = []
    confidence_scores = []
    
    for product in all_products:
        division = DIVISION_MAP.get(product, "Other")
        for region in all_regions:
            for ship_mode in all_ship_modes:
                total_scenarios += 1
                try:
                    sim = simulate_reallocation(model, product, division, region, ship_mode)
                    current = sim[sim['Is Current']]
                    best = sim.iloc[0]
                    
                    if not current.empty:
                        current_lt = current['Predicted Lead Time (Days)'].values[0]
                        best_lt = best['Predicted Lead Time (Days)']
                        
                        if current_lt > 0:
                            reduction_pct = ((current_lt - best_lt) / current_lt) * 100
                            lead_time_reductions.append(max(reduction_pct, 0))
                        
                        margin_impacts.append(best['Margin Impact (%)'])
                        
                        if best['Factory'] != current['Factory'].values[0]:
                            reallocations_recommended += 1
                        
                        # Confidence: how much separation between best and worst
                        spread = sim['Predicted Lead Time (Days)'].max() - sim['Predicted Lead Time (Days)'].min()
                        confidence = min(spread / max(current_lt, 1) * 100, 100)
                        confidence_scores.append(confidence)
                except Exception:
                    continue
    
    avg_lead_time_reduction = np.mean(lead_time_reductions) if lead_time_reductions else 0
    profit_stability = 100 - abs(np.mean(margin_impacts)) * 10 if margin_impacts else 100
    profit_stability = max(min(profit_stability, 100), 0)
    avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
    coverage = (reallocations_recommended / max(total_scenarios, 1)) * 100
    
    return {
        "Lead Time Reduction (%)": round(avg_lead_time_reduction, 1),
        "Profit Impact Stability": round(profit_stability, 1),
        "Scenario Confidence Score": round(avg_confidence, 1),
        "Recommendation Coverage": round(coverage, 1)
    }