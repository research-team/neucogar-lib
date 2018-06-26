import os
import pylab
import numpy as np
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


def read_data(path):
	"""
	Collect and sort data from the file
	Args:
		path (str): path to the file

	Returns:
		dict: key - timestep, value - data list of each core
	"""
	time_step = 0
	data_per_timestep = {}
	# Read file
	with open(path, 'r') as file:
		for line in file:
			float_data = []
			# Drop another, non informative data
			if line.startswith("MPI"):
				for data in line.split("  "):
					if not data.startswith("MPI"):
						float_data.append(float(data[:-3]) if "MB" in data else float(data))
				data_per_timestep[time_step] = float_data
				time_step += 10
	return data_per_timestep


def collect_data(raw_data, mean=False):
	"""
	Sorting and compute the data by variables

	Args:
		raw_data (dict): time and core data
		mean (bool): True - calculate the mean value per core, False - calculate separatelly

	Returns:

	"""
	mem = []
	time = []
	cores = len(raw_data[0][:-1])

	sorted_data = sorted(raw_data.items())

	for time_step, data in sorted_data:
		time.append(time_step)
		mem.append(data[-1])

	if mean:
		cpu = []
		for time_step, data in sorted_data:
			cpu.append(sum(data[:-1]) / len(data[:-1]))
	else:
		# Create a void dict with key = core index
		cpu = { core_index : [] for core_index in range(cores) }
		for time_step, data in sorted_data:
			for core_index, core_data in enumerate(data[:-1]):
				cpu[core_index].append(core_data)
	return cpu, mem, time


def draw(cpu, mem, time, neuroblocks_data, T=1000, with_RAM=False, save=True):
	"""
	Visualize the data
	Args:
		cpu (dict): data per timestamp and core
		mem (list): data of memory usage
		time (list): timestemps
		neuroblocks_data (dict): structure of figures
		T (float): time simulation
		with_RAM (bool): True - draw with RAM, False - draw without RAM
		save (bool): True - save the results, False - only show

	Returns:
		None
	"""
	xtick_step = 250
	yticks_number = 16

	pylab.ioff()
	if with_RAM:
		f, (ax1, ax2) = pylab.subplots(2, 1, sharex='all', figsize=(16, 9))
	else:
		f, ax1 = pylab.subplots(1, 1, sharex='all', figsize=(16, 9))
		ax2 = None

	max_cpu = max(cpu)
	min_cpu = min(cpu)

	# Set Y ticks and get the step
	yticks = np.arange(min_cpu, max_cpu+1, (max_cpu - min_cpu)  / yticks_number)
	ytick_step = yticks[1] - yticks[0]

	# Set block size
	block_height = ytick_step
	block_width = xtick_step

	# CPU subplot
	ax1.set_ylabel('CPU time (s)')
	ax1.set_xlim([0, max(time)+1])
	ax1.set_ylim(min_cpu, max_cpu)
	ax1.set_yticks(yticks)
	ax1.grid(which='minor', alpha=0.2)
	ax1.grid(which='major', alpha=0.5)
	if type(cpu) == list:
		# Draw mean value
		ax1.plot(time, cpu, "r", linewidth=0.7)
	else:
		# Draw per core
		for core_index, core_data in cpu.items():
			ax1.plot(time, core_data, "", linewidth=0.7)

	# Draw the blocks
	for n_time, elements in neuroblocks_data.items():
		# Set the start position of the block
		start_point_X = n_time
		start_point_Y = yticks[0]
		# Draw each block
		for element in elements:
			name = element[0]
			modulator_level = element[1]
			ax1.add_patch(
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

	if with_RAM:
		# MEM subplot
		ax2.set_xlabel('Simulation time (ms)')
		ax2.set_ylabel('RAM (MB)')
		ax2.set_xlim([0, max(time)+10])
		ax2.grid(which='minor', alpha=0.2)
		ax2.grid(which='major', alpha=0.5)
		ax2.plot(time, mem, "", linewidth=1)
	else:
		ax1.set_xlabel('Simulation time (ms)')

	# Common settings
	pylab.xticks(np.arange(0, T + 1, xtick_step))
	pylab.xticks(rotation=90)


	# Actions with image
	f.subplots_adjust(left=0.05, bottom=0.1, right=0.96, top=0.99, wspace=0.0, hspace=0.05)
	if save:
		pylab.savefig("CPU.pdf", dpi=300, format='pdf')
	pylab.show()
	pylab.clf()


def start():
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

	path = input("Enter path to the file with '.out' format")
	raw_data = read_data(path)
	cpu, mem, time = collect_data(raw_data, mean=True)
	draw(cpu, mem, time, time2neuro, T=21000, with_RAM=False, save=False)


if __name__ == "__main__":
	start()