from geopy.distance import geodesic

class RoutingEngine:
    def __init__(self, ports_data):
        self.ports = ports_data

    def calculate_astar_path(self, start_port, end_port, weather_val, traffic_val, fuel_priority):
        start_coords = self.ports[start_port]
        end_coords = self.ports[end_port]
        
        base_dist = geodesic(start_coords, end_coords).km
        
        # Versatile Cost Calculation
        weather_penalty = (weather_val - 1) * 0.10
        traffic_penalty = (traffic_val - 1) * 0.05
        g_n = base_dist * (1 + weather_penalty + traffic_penalty)
        
        fuel_rate = 0.12 if fuel_priority else 0.18
        total_fuel = g_n * fuel_rate
        
        speed = 30 if fuel_priority else 45
        h_n = g_n / speed 
        
        return {
            "path": [start_coords, end_coords],
            "base_dist": round(base_dist, 2),
            "optimized_cost": round(g_n, 2),
            "fuel_tons": round(total_fuel, 2),
            "eta_hrs": round(h_n, 1)
        }