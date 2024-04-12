original_list = [[1, 2], [1, 2], [3, 4]]
deduplicated_list = list(set(tuple(sorted(sublist)) for sublist in original_list))
print(deduplicated_list)