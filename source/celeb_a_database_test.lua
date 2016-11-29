require('image')
local F = require('F')

local function to_uint32(a, b, c, d)
	return bit.lshift(d, 24) + bit.lshift(c, 16) + bit.lshift(b, 8) + a
end

local function next_uint32(data, off)
	return to_uint32(string.byte(data, off), string.byte(data, off + 1),
		string.byte(data, off + 2), string.byte(data, off + 3))
end

local function parse_info(info_file_path)
	local data = io.open(info_file_path, 'rb'):read('*all')
	local entry_count = next_uint32(data, 1)
	print(F"Total number of entries: {entry_count}.")

	local data_off      = 5
	local jpg_off       = 1
	local entries       = {}
	local id_to_entries = {}

	for i = 1, entry_count do
		local id = next_uint32(data, data_off)
		assert(id >= 0)
		data_off = data_off + 4

		local size = next_uint32(data, data_off)
		assert(size >= 1)
		data_off = data_off + 4

		id_to_entries[id + 1] = id_to_entries[id + 1] or {}
		table.insert(id_to_entries[id + 1], i)

		table.insert(entries, {id = id + 1, start = jpg_off, end_ = jpg_off + size - 1})
		jpg_off = jpg_off + size
	end

	return entries, id_to_entries
end

local function parse_data(data_file_path)
	return torch.ByteTensor(torch.ByteStorage():string(
		io.open(data_file_path, 'rb'):read('*all')))
end

local function save_sample_uncond_batch(output_dir, entries, data)
	for i = 1, 30 do
		local e = entries[i]
		local img = image.decompressJPG(data[{{e.start, e.end_}}])
		local img_path = paths.concat(output_dir, F'{i}.jpg')
		image.save(img_path, img)
	end
end

local function save_sample_cond_batch(output_dir, entries, id_to_entries, data)
	for i, id_ in pairs(id_to_entries[20]) do
		local entry = entries[id_]
		local img = image.decompressJPG(data[{{entry.start, entry.end_}}])
		local img_path = paths.concat(output_dir, F'{i}.jpg')
		image.save(img_path, img)
	end
end

local output_dir     = 'output/celeb_a_database_test'
local info_file_path = 'output/celeb_a_info.bin'
local data_file_path = 'output/celeb_a_data.bin'
local uncond_dir     = paths.concat(output_dir, 'uncond')
local cond_dir       = paths.concat(output_dir, 'cond')

assert(not paths.dirp(output_dir))
assert(not paths.dirp(uncond_dir))
assert(not paths.dirp(cond_dir))

paths.mkdir(output_dir)
paths.mkdir(uncond_dir)
paths.mkdir(cond_dir)

local entries, id_to_entries = parse_info(info_file_path)
local data = parse_data(data_file_path, info)

local count = 0
local threshold = 8

for id, entry in pairs(id_to_entries) do
	if #entry >= threshold then count = count + 1 end
end

print(F"{count} / {#id_to_entries} entries have more than {threshold} instances.")

print("Saving unconditional batch.")
save_sample_uncond_batch(uncond_dir, entries, data)

print("Saving conditional batch.")
save_sample_cond_batch(cond_dir, entries, id_to_entries, data)
