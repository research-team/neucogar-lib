import os
import numpy as np
import pylab as plt
import matplotlib.patches as patches

DA = "DA"
HT5 = "5HT"
NA = "NA"

def get_hex(n):
	if n == "DA":
		return "#bde4b9"
	elif n == "5HT":
		return "#e9b9ff"
	else:
		return "#fff4b9"


def collect_data(path):
	"""
	Gather data of all .gdf files in the "path" folder

	Args:
		path (str): path to the folder with .gdf files

	Returns:
		list : all gathered data in one variable
	"""
	data = []
	files = sorted([name for name in os.listdir(path) if name.endswith(".gdf")])

	if files:
		for file in files:
			with open("{}/{}".format(path, file), 'r') as f:
				data += [float(i.split("\t")[1]) if len(i) > 5 else 0 for i in f.read().split("\n")]
		return data
	else:
		raise UserWarning("There are no files with .gdf!")


def draw(spikes_data, neuroblocks_data, save=False, binwidth=5.0, T=1000):
	"""
	Drawing the figure

	Args:
		spikes_data (list): time list of spikes
		neuroblocks_data (dict): data of neuromodulators activation time
		save (bool): True - save as .pdf, False - no saving
		binwidth (float): size of the bin
		T (float): simulation time

	Returns:
		None
	"""

	xtick_step = 250
	yticks_number = 16

	plt.close("all")
	# Create the figure
	fig, ax = plt.subplots(1, figsize=(16, 9))
	fig.subplots_adjust(left=0.05, bottom=0.1, right=0.99, top=0.99, wspace=0.0, hspace=0.0)
	# Draw the histogram
	n, bins, p = ax.hist(sorted(spikes_data), bins=np.arange(min(spikes_data), max(spikes_data) + binwidth, binwidth))

	# Save max/min values
	max_value = max(n)
	min_value = min(n)

	# Set Y ticks and get the step
	yticks = np.arange(min_value, max_value, max_value / yticks_number)
	ytick_step = yticks[1] - yticks[0]

	# Set block size
	block_height = ytick_step
	block_width = xtick_step

	# Draw the blocks
	for time, elements in neuroblocks_data.items():
		# Set the start position of the block
		start_point_X = time
		start_point_Y = min_value
		# Draw each block
		for element in elements:
			name = element[0]
			modulator_level = element[1]
			ax.add_patch(
				patches.Rectangle(
					(start_point_X, start_point_Y),
					block_width,
					block_height * modulator_level,
					facecolor=get_hex(name),
					alpha=0.95
				),
			)
			# Change the Y start position
			start_point_Y += block_height * modulator_level

	# Tune a X axis
	ax.set_xlim(0, T)
	ax.set_xticks(np.arange(0, T + 1, xtick_step))
	ax.set_xticklabels(np.arange(0, T + 1, xtick_step), rotation=90)
	ax.set_xlabel('Simulation time (ms)')
	# Tune an Y axis
	ax.set_ylim(0, max(n))
	ax.set_yticks(yticks)
	ax.set_ylabel('Spikes (count)')
	# Tune a grid
	ax.grid(which='minor', alpha=0.2)
	ax.grid(which='major', alpha=0.5)

	# Actions with results
	if save:
		plt.savefig("spikes.pdf", dpi=300, format='pdf')
	plt.show()
	plt.clf()


def run():
	# dict of time and neuromodulators
	time2neuro = {1250: [(NA, 1)],
	              2000: [(NA, 2)],
	              2750: [(HT5, 1)],
	              3500: [(HT5, 1), (NA, 1)],
	              4250: [(HT5, 1), (NA, 2)],
	              5000: [(HT5, 2)],
	              5750: [(HT5, 2), (NA, 1)],
	              6500: [(HT5, 2), (NA, 2)],
	              7250: [(DA, 1)],
	              8000: [(DA, 1), (NA, 1)],
	              8750: [(DA, 1), (NA, 2)],
	              9500: [(DA, 1), (HT5, 1)],
	              10250: [(DA, 1), (HT5, 1), (NA, 1)],
	              11000: [(DA, 1), (HT5, 1), (NA, 2)],
	              11750: [(DA, 1), (HT5, 2)],
	              12500: [(DA, 1), (HT5, 2), (NA, 1)],
	              13250: [(DA, 1), (HT5, 2), (NA, 2)],
	              14000: [(DA, 2)],
	              14750: [(DA, 2), (NA, 1)],
	              15500: [(DA, 2), (NA, 2)],
	              16250: [(DA, 2), (HT5, 1)],
	              17000: [(DA, 2), (HT5, 1), (NA, 1)],
	              17750: [(DA, 2), (HT5, 1), (NA, 2)],
	              18500: [(DA, 2), (HT5, 2)],
	              19250: [(DA, 2), (HT5, 2), (NA, 1)],
	              20000: [(DA, 2), (HT5, 2), (NA, 2)],
	              }

	path = input("Enter path to the result folder")
	data = collect_data(path)
	draw(data, time2neuro, save=False, T=21000)


if __name__ == "__main__":
	run()