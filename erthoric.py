#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Erthoric - Earthquake Monitoring System
Developer: EbiRom96
GitHub: https://github.com/EbiRom96
Contact: Raptor96@nixom.ir, Orion.GodRaptor@hotmail.com
Version: 1.0.0
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta
import sys
import subprocess

class Erthoric:
    def __init__(self):
        self.base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
        self.continent_data = {
            "Asia": ["JP", "CN", "IN", "ID", "PH", "VN", "TH", "KR", "IR", "TR"],
            "Europe": ["IT", "GR", "IS", "PT", "ES", "FR", "DE", "GB", "RO"],
            "North America": ["US", "CA", "MX", "JM", "GT", "CR"],
            "South America": ["CL", "PE", "EC", "CO", "AR", "BR", "BO"],
            "Oceania": ["NZ", "PG", "FJ", "SB", "VU"],
            "Africa": ["DZ", "EG", "ET", "KE", "ZA", "MG"]
        }
        self.alerts = []
        self.version = "1.0.0"
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        header = f"""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    ███████╗██████╗ ████████╗██╗  ██╗ ██████╗ ██████╗ ██╗ ██████╗║
║    ██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██║██╔════╝║
║    █████╗  ██████╔╝   ██║   ███████║██║   ██║██████╔╝██║██║     ║
║    ██╔══╝  ██╔══██╗   ██║   ██╔══██║██║   ██║██╔══██╗██║██║     ║
║    ███████╗██║  ██║   ██║   ██║  ██║╚██████╔╝██║  ██║██║╚██████╗║
║    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝║
║                                                                ║
║                 Real-time Earthquake Monitor                   ║
║                         Version {self.version}                         ║
║                    Developer: EbiRom96                         ║
║               GitHub: https://github.com/EbiRom96              ║
║          Contact: Raptor96@nixom.ir, Orion.GodRaptor@hotmail.com║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(header)
    
    def get_earthquake_data(self):
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data: {e}")
            print("🔧 Please check your internet connection and try again.")
            return None
    
    def format_magnitude(self, mag):
        if mag >= 6.0:
            return f"🔴 {mag:.1f} (Strong)"
        elif mag >= 4.5:
            return f"🟡 {mag:.1f} (Moderate)"
        else:
            return f"🟢 {mag:.1f} (Light)"
    
    def format_time(self, timestamp):
        quake_time = datetime.fromtimestamp(timestamp / 1000)
        now = datetime.now()
        diff = now - quake_time
        
        if diff < timedelta(minutes=1):
            return "Just now"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minute(s) ago"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hour(s) ago"
        else:
            return quake_time.strftime("%Y-%m-%d %H:%M")
    
    def display_all_earthquakes(self, data):
        print("\n🌍 Recent Earthquakes (Last Hour)")
        print("=" * 80)
        
        features = data.get('features', [])
        if not features:
            print("❌ No earthquakes recorded in the last hour.")
            return
        
        print(f"{'Location':<30} {'Magnitude':<15} {'Time':<20} {'Depth (km)':<10}")
        print("-" * 80)
        
        for feature in features[:20]:
            props = feature['properties']
            geometry = feature['geometry']
            
            place = props['place'][:28] + "..." if len(props['place']) > 28 else props['place']
            mag = self.format_magnitude(props['mag'])
            time_str = self.format_time(props['time'])
            depth = f"{geometry['coordinates'][2]:.1f}"
            
            print(f"{place:<30} {mag:<15} {time_str:<20} {depth:<10}")
    
    def display_continent_earthquakes(self, data, continent):
        print(f"\n🌍 Earthquakes in {continent}")
        print("=" * 80)
        
        features = data.get('features', [])
        if not features:
            print("❌ No earthquakes recorded in the last hour.")
            return
        
        continent_countries = self.continent_data.get(continent, [])
        continent_quakes = []
        
        for feature in features:
            props = feature['properties']
            place = props['place'].upper()
            
            for country_code in continent_countries:
                if country_code in place:
                    continent_quakes.append(feature)
                    break
        
        if not continent_quakes:
            print(f"❌ No earthquakes in {continent} in the last hour.")
            return
        
        print(f"{'Location':<30} {'Magnitude':<15} {'Time':<20} {'Depth (km)':<10}")
        print("-" * 80)
        
        for feature in continent_quakes[:15]:
            props = feature['properties']
            geometry = feature['geometry']
            
            place = props['place'][:28] + "..." if len(props['place']) > 28 else props['place']
            mag = self.format_magnitude(props['mag'])
            time_str = self.format_time(props['time'])
            depth = f"{geometry['coordinates'][2]:.1f}"
            
            print(f"{place:<30} {mag:<15} {time_str:<20} {depth:<10}")
    
    def display_largest_earthquakes(self, data):
        print("\n💥 Largest Recent Earthquakes")
        print("=" * 80)
        
        features = data.get('features', [])
        if not features:
            print("❌ No earthquakes recorded in the last hour.")
            return
        
        sorted_quakes = sorted(features, key=lambda x: x['properties']['mag'], reverse=True)
        
        print(f"{'Location':<30} {'Magnitude':<15} {'Time':<20} {'Depth (km)':<10}")
        print("-" * 80)
        
        for feature in sorted_quakes[:10]:
            props = feature['properties']
            geometry = feature['geometry']
            
            place = props['place'][:28] + "..." if len(props['place']) > 28 else props['place']
            mag = self.format_magnitude(props['mag'])
            time_str = self.format_time(props['time'])
            depth = f"{geometry['coordinates'][2]:.1f}"
            
            print(f"{place:<30} {mag:<15} {time_str:<20} {depth:<10}")
    
    def set_city_alert(self):
        print("\n🔔 Set City Alert")
        print("=" * 40)
        
        city = input("Enter city name: ").strip()
        if not city:
            print("❌ City name cannot be empty.")
            return
        
        try:
            min_magnitude = float(input("Enter minimum magnitude for alert (e.g., 4.5): "))
        except ValueError:
            print("❌ Invalid magnitude. Please enter a number.")
            return
        
        alert = {
            'city': city.upper(),
            'min_magnitude': min_magnitude,
            'created_at': datetime.now()
        }
        
        self.alerts.append(alert)
        print(f"✅ Alert set for {city} (Magnitude ≥ {min_magnitude})")
    
    def check_alerts(self, data):
        if not self.alerts:
            return
        
        features = data.get('features', [])
        if not features:
            return
        
        print("\n🚨 ALERT NOTIFICATIONS")
        print("=" * 50)
        
        for alert in self.alerts:
            city = alert['city']
            min_mag = alert['min_magnitude']
            
            for feature in features:
                props = feature['properties']
                if (city in props['place'].upper() and 
                    props['mag'] >= min_mag):
                    
                    print(f"⚠️  ALERT: Earthquake in {props['place']}!")
                    print(f"   Magnitude: {props['mag']} | Time: {self.format_time(props['time'])}")
                    print("-" * 50)
    
    def display_menu(self):
        print("\n" + "=" * 50)
        print("📋 MAIN MENU")
        print("=" * 50)
        print("1. 🌍 Show All Recent Earthquakes")
        print("2. 🗺️  Show Earthquakes by Continent")
        print("3. 💥 Show Largest Earthquakes")
        print("4. 🔔 Set City Alert")
        print("5. 📊 Show Active Alerts")
        print("6. 🔄 Refresh Data")
        print("7. ℹ️  About & Version")
        print("8. 🚪 Exit")
        print("=" * 50)
    
    def show_about(self):
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║                         ABOUT ERTHORIC                        ║
╚════════════════════════════════════════════════════════════════╝

Version: {self.version}
Developer: EbiRom96
GitHub: https://github.com/EbiRom96
Contact: Raptor96@nixom.ir, Orion.GodRaptor@hotmail.com

Description:
Erthoric is a real-time earthquake monitoring system that displays
live earthquake data from around the world using the USGS API.

Features:
• Real-time earthquake data
• Continental filtering
• Largest earthquakes view
• Custom city alerts
• Cross-platform compatibility

Data Source: United States Geological Survey (USGS)
License: MIT
        """)
    
    def run(self):
        while True:
            self.clear_screen()
            self.display_header()
            
            data = self.get_earthquake_data()
            if data:
                self.check_alerts(data)
                self.display_menu()
                
                choice = input("\nEnter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.display_all_earthquakes(data)
                elif choice == '2':
                    print("\n🌐 Select Continent:")
                    continents = list(self.continent_data.keys())
                    for i, continent in enumerate(continents, 1):
                        print(f"{i}. {continent}")
                    
                    try:
                        cont_choice = int(input(f"\nSelect continent (1-{len(continents)}): "))
                        if 1 <= cont_choice <= len(continents):
                            self.display_continent_earthquakes(data, continents[cont_choice-1])
                        else:
                            print("❌ Invalid continent selection.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
                elif choice == '3':
                    self.display_largest_earthquakes(data)
                elif choice == '4':
                    self.set_city_alert()
                elif choice == '5':
                    print("\n📊 Active Alerts:")
                    if not self.alerts:
                        print("No active alerts.")
                    else:
                        for i, alert in enumerate(self.alerts, 1):
                            print(f"{i}. {alert['city']} (Mag ≥ {alert['min_magnitude']}) - Created: {alert['created_at'].strftime('%Y-%m-%d %H:%M')}")
                elif choice == '6':
                    print("🔄 Refreshing data...")
                    continue
                elif choice == '7':
                    self.show_about()
                elif choice == '8':
                    print("👋 Thank you for using Erthoric! Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            else:
                print("❌ Failed to fetch earthquake data. Please check your internet connection.")
            
            input("\nPress Enter to continue...")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import requests
        return True
    except ImportError:
        print("❌ Required package 'requests' is not installed.")
        print("Please install it using: pip install requests")
        return False

def main():
    # For EXE version, don't check dependencies as they're included
    app = Erthoric()
    app.run()

if __name__ == "__main__":
    main()