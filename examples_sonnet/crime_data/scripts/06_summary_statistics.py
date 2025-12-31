import pandas as pd
import numpy as np

# Load data
df = pd.read_parquet('/Users/yegorklochkov/repos/eda_agent/test/crime_data/Crime_Data_from_2020_to_Present.parquet')
df['hour'] = df['TIME OCC'].apply(lambda x: x.hour)

print("=" * 80)
print("COMPREHENSIVE STATISTICAL SUMMARY")
print("=" * 80)

print("\n1. DATASET OVERVIEW")
print(f"   Total records: {len(df):,}")
print(f"   Date range: {df['DATE OCC'].min().date()} to {df['DATE OCC'].max().date()}")
print(f"   Number of columns: {len(df.columns)}")
print(f"   Exact duplicates: {df.duplicated().sum()}")

print("\n2. TEMPORAL STATISTICS")
print(f"   Peak crime hour: {df['hour'].value_counts().idxmax()}:00 ({df['hour'].value_counts().max():,} crimes)")
print(f"   Lowest crime hour: {df['hour'].value_counts().idxmin()}:00 ({df['hour'].value_counts().min():,} crimes)")
day_counts = df['occ_day'].value_counts()
print(f"   Most crimes day: {day_counts.idxmax()} ({day_counts.max():,} crimes)")
print(f"   Least crimes day: {day_counts.idxmin()} ({day_counts.min():,} crimes)")
year_counts = df['occ_year'].value_counts().sort_index()
print(f"   Crimes per year: {year_counts.to_dict()}")

print("\n3. CRIME TYPE STATISTICS")
print(f"   Total crime types: {df['Crm Cd Desc'].nunique()}")
print(f"   Most common crime: {df['Crm Cd Desc'].value_counts().idxmax()}")
print(f"   Frequency: {df['Crm Cd Desc'].value_counts().max():,} ({df['Crm Cd Desc'].value_counts().max()/len(df)*100:.1f}%)")
print(f"   Part 1 (Serious) crimes: {(df['Part 1-2'] == 1).sum():,} ({(df['Part 1-2'] == 1).sum()/len(df)*100:.1f}%)")
print(f"   Part 2 crimes: {(df['Part 1-2'] == 2).sum():,} ({(df['Part 1-2'] == 2).sum()/len(df)*100:.1f}%)")

# Concentration analysis
crime_counts = df['Crm Cd Desc'].value_counts()
cumsum = crime_counts.cumsum() / len(df) * 100
pct_50 = (cumsum <= 50).sum()
pct_80 = (cumsum <= 80).sum()
print(f"   Top {pct_50} crime types account for 50% of all crimes")
print(f"   Top {pct_80} crime types account for 80% of all crimes")

print("\n4. VICTIM STATISTICS")
age_valid = df[df['Vict Age'] > 0]['Vict Age']
print(f"   Age = 0 (unknown): {(df['Vict Age'] == 0).sum():,} ({(df['Vict Age'] == 0).sum()/len(df)*100:.1f}%)")
print(f"   Negative ages: {(df['Vict Age'] < 0).sum()}")
print(f"   Valid age range: {age_valid.min()} to {age_valid.max()}")
print(f"   Median age: {age_valid.median():.0f}")
print(f"   Mean age: {age_valid.mean():.1f}")
print("\n   Sex distribution:")
for sex, count in df['Vict Sex'].value_counts().items():
    print(f"      {sex}: {count:,} ({count/len(df)*100:.1f}%)")

print("\n5. LOCATION STATISTICS")
print(f"   LAPD Areas: {df['AREA NAME'].nunique()}")
area_counts = df['AREA NAME'].value_counts()
print(f"   Highest crime area: {area_counts.idxmax()} ({area_counts.max():,} crimes)")
print(f"   Lowest crime area: {area_counts.idxmin()} ({area_counts.min():,} crimes)")
print(f"   Missing coordinates: {(df['LAT'] == 0).sum():,} ({(df['LAT'] == 0).sum()/len(df)*100:.2f}%)")
print(f"   Total premise types: {df['Premis Desc'].nunique()}")
print(f"   Most common premise: {df['Premis Desc'].value_counts().idxmax()} ({df['Premis Desc'].value_counts().max():,})")

print("\n6. WEAPON STATISTICS")
unknown_weapons = (df['Weapon Desc'] == 'Unknown').sum()
print(f"   Unknown weapon: {unknown_weapons:,} ({unknown_weapons/len(df)*100:.1f}%)")
weapon_known = df[df['Weapon Desc'] != 'Unknown']
if len(weapon_known) > 0:
    print(f"   Most common weapon: {weapon_known['Weapon Desc'].value_counts().idxmax()}")
    print(f"   Frequency: {weapon_known['Weapon Desc'].value_counts().max():,}")

print("\n7. CASE STATUS")
for status, count in df['Status Desc'].value_counts().items():
    print(f"   {status}: {count:,} ({count/len(df)*100:.1f}%)")

total_arrests = df[df['Status Desc'].str.contains('Arrest', na=False)]
print(f"   Total arrests: {len(total_arrests):,} ({len(total_arrests)/len(df)*100:.1f}%)")

print("\n8. REPORTING DELAY")
df['report_delay_days'] = (df['Date Rptd'] - df['DATE OCC']).dt.days
delay_valid = df[df['report_delay_days'] >= 0]['report_delay_days']
print(f"   Median delay: {delay_valid.median():.0f} days")
print(f"   Mean delay: {delay_valid.mean():.1f} days")
print(f"   Same-day reports: {(delay_valid == 0).sum():,} ({(delay_valid == 0).sum()/len(delay_valid)*100:.1f}%)")
print(f"   Reported within 7 days: {(delay_valid <= 7).sum():,} ({(delay_valid <= 7).sum()/len(delay_valid)*100:.1f}%)")
print(f"   Reported after 1 year: {(delay_valid > 365).sum():,} ({(delay_valid > 365).sum()/len(delay_valid)*100:.1f}%)")

print("\n" + "=" * 80)
