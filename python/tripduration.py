import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data into a DataFrame
df = pd.read_csv("../dependencies/July.csv")

# Filter the DataFrame to include only rows where 'member_casual' is 'member'
df = df[df['member_casual'] == 'member']

# Convert 'started_at' and 'ended_at' columns to datetime objects
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])

# Calculate trip durations in minutes
df['trip_duration_minutes'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# total_minutes = df['trip_duration_minutes'].sum()

# print("Total minutes is " + total_minutes)

# Define custom bin edges
x_bin_edges = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

y_bin_edges = np.arange(0, 225000, 25000)


# Plot a histogram of trip durations in minutes with custom bins
plt.hist(df['trip_duration_minutes'], bins=x_bin_edges, color='blue')
plt.xlabel('Trip Duration (minutes)')
plt.ylabel('Frequency')
plt.title('Frequency of Bike Rides Sorted by Trip Durations for members for July')
plt.xticks(x_bin_edges)  # Set x-axis tick marks to match bin edges
plt.yticks(y_bin_edges)
plt.grid(axis='x')     # Add gridlines along x-axis

#members is blue 
#casual is red
#total is purple 


plt.savefig('bike_rides_histogram_members.png')

plt.show()




