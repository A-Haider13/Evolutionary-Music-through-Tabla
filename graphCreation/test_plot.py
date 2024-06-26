import matplotlib.pyplot as plt

# Define the ratios and corresponding results
ratios = ['0.05','0.1','0.2', '0.25','0.3', '0.33','0.4','0.45','0.5','0.6','0.7','0.75','0.8','0.9','0.95','1']
result1 = [232.63,220.25,215.56, 212.87,210.88, 210.37, 209.04, 209.52, 209.38,209.50,208.34,208.74,208.42,206.19,207.63,206.11]
result2 = [43,40,44, 40,43, 44, 43, 44, 43,42,43,43,45,43,43,46]
mutation_rates = ['0.2','0.3','0.4','0.5','0.6','0.7','0.8']
result3 = [213.84,214.97,219.72,219.17,221.75,222.90,221.86]
result4 = [44,45,43,40,42,42,43]
# result2 = [i*5 for i in result2] #multiplying by 5 to make the results more visible

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(mutation_rates, result3, marker='o', label='Result 1', color='b')
# plt.plot(ratios, result2, marker='o', label='Result 2', color='g')

# Add titles and labels
plt.title('Comparison of Results for Different Ratios')
plt.xlabel('Ratios')
plt.ylabel('Results')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
