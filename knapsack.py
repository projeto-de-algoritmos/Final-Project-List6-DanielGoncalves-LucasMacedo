def knapsack(avaliable_weight, weights, values, items_quantity):
    matrix = [[0 for x in range(avaliable_weight + 1)] for x in range(items_quantity + 1)]

    for item in range(1, items_quantity + 1):
        for weight in range(1, avaliable_weight + 1):
            if weights[item - 1] <= weight:
                matrix[item][weight] = max(values[item - 1] + matrix[item - 1][weight - weights[item - 1]], matrix[item - 1][weight])
            else:
                matrix[item][weight] = matrix[item - 1][weight]

    return matrix, matrix[items_quantity][avaliable_weight]

def find_solution(matrix, weights, items_quantity, avaliable_weight):
    init = matrix[items_quantity][avaliable_weight]
    items_taken = []

    item = items_quantity
    weight = avaliable_weight

    while item != 0 and weight != 0:
        if matrix[item - 1][weight] < matrix[item][weight]:
            items_taken.append(item)
            weight -= weights[item - 1]
            item -= 1
        else:
            item = item - 1

    return items_taken

values = [1, 6, 18, 22, 28] 
weights = [1, 2, 5, 6, 7] 
avaliable_weight = 11
items_quantity = len(values)

matrix, max_value = knapsack(avaliable_weight, weights, values, items_quantity)

items_taken = find_solution(matrix, weights, items_quantity, avaliable_weight)

print(matrix)
print(max_value)
print(items_taken)