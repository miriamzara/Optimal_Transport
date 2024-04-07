import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
data_histo_1=np.loadtxt('gauss1_100.txt')
data_histo_2=np.loadtxt('gauss2_100.txt')
X1=data_histo_1[:,0]
Y1=data_histo_1[:,1]
X2=data_histo_2[:,0]
Y2=data_histo_2[:,1]
numero_bin=len(X1)

numero_bin=len(X1)
# Read the data from the text file
with open('OT_FREE_SCALING_reset_100_piano_trasporto_1e+06.txt', 'r') as file:
    lines = file.readlines()
# Initialize empty lists for the data sections
data = []
current_section = []  # Temporary list to hold each section of data
# Iterate through the lines and populate the data list with sections
for line in lines:
    line = line.strip()  # Remove leading/trailing whitespaces
    if not line:  # Check for an empty line separating sections
        if current_section:  # If the section isn't empty
            data.append(current_section)  # Append to data list
            current_section = []  # Reset the temporary list for the next section
        continue
    current_section.append(float(line))  # Append the line to the current section
# Append the last section after the loop ends
if current_section:
    data.append(current_section)
# Convert the data list to a NumPy array
matrix = np.array(data)



fig=plt.figure(figsize=(10,10))
gs=fig.add_gridspec(3,3, hspace=0, wspace=0)
ax1 = fig.add_subplot (gs [0, 1:])
ax1.bar(X2,Y2, width=100./numero_bin, align="edge")
ax1.set_xlim(0,100)
ax1.xaxis.tick_top()
ax1.set_xticks(np.arange(0, 110, 10))
ax1.set_yticks(np.linspace(0.001, np.max(Y2),3))
ax1.tick_params(axis='y', direction= 'in', pad=-50 )

ax2 = fig.add_subplot (gs [1:, 0])
ax2.barh(X1,Y1, height=100./numero_bin, align="edge", color='red')
ax2.set_yticks(np.arange(0,110, 10))
ax2.set_ylim(0,100)
ax2.invert_yaxis()
ax2.invert_xaxis()
ax2.set_xticks(np.linspace(0.001, np.max(Y1), 3))
ax2.xaxis.tick_top()

ax3 = fig.add_subplot (gs [1:,1:])
im=ax3.imshow(matrix, cmap='Greys')
#creazione griglia
# Minor ticks
ax3.set_xticks(np.arange(-0.5, numero_bin, 1), minor=True)
ax3.set_yticks(np.arange(-0.5, numero_bin, 1), minor=True)
# Gridlines based on minor ticks
ax3.grid(which='minor', color='dimgray', linestyle='-', linewidth=0.1)
# Remove minor ticks
ax3.tick_params(which='minor', bottom=False, left=False)

#creazione colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # Define position and size of the colorbar axis
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label("massa trasportata")


ax3.set_xticks([])
ax3.set_yticks([])

plt.suptitle('parametro $beta=1e+06$, costo p=2', fontsize=16,x=0.2,y=0.95)

plt.savefig('OT_FREE_SCALING_reset_beta_1e+06.png', bbox_inches='tight')
plt.show()