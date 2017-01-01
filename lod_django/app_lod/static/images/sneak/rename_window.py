import os

i = 0

for filename in os.listdir("."):
	if filename.endswith("_sneak.png"):
		# Slice it with "_"
		# 1 > "", 2 > number, 3 > champion, 4 > extension
		bits = filename.split("_")
		if len(bits) == 2:
			i += 1
			final = bits[0] + ".png"
			os.rename(filename, final)
			print(i, "Origin", filename, "final", final)
