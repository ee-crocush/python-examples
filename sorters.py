# Сортировка пузырьком
def bubble_sort(source_a: list) -> list:
    a = [i for i in source_a]
    for i in range(len(a)):
        for j in range(len(a) - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


# Сортировка выбором
def selection_sort(source_a: list) -> list:
    a = [i for i in source_a]

    for i in range(len(a)):
        min_index = i
        for j in range(i + 1, len(a)):
            if a[j] < a[min_index]:
                min_index = j
        a[i], a[min_index] = a[min_index], a[i]
    return a


# Сортировка выбором двунаправленная
def bi_selection_sort(source_a: list) -> list:
    arr = [i for i in source_a]
    n = len(arr)
    left, right = 0, n - 1

    while left < right:
        min_index, max_index = left, right

        for i in range(left, right + 1):
            if arr[i] < arr[min_index]:
                min_index = i
            if arr[i] > arr[max_index]:
                max_index = i

        arr[left], arr[min_index] = arr[min_index], arr[left]

        if max_index == left:
            max_index = min_index

        arr[right], arr[max_index] = arr[max_index], arr[right]

        left += 1
        right -= 1
    return arr


# Сортировка вставками
def insert_sort(source_a: list) -> list:
    arr = [i for i in source_a]

    for i in range(1, len(arr)):
        c = arr[i]
        j = i - 1

        while j >= 0 and c <= arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = c

    return arr


# Сортировка слиянием
def merge_sort(source_a: list) -> list:
    arr = [i for i in source_a]

    if len(arr) <= 1:
        return arr

    mid = len(source_a) // 2
    left_arr = merge_sort(arr[:mid])
    right_arr = merge_sort(arr[mid:])

    return sub_merge_sort(left_arr, right_arr)


def sub_merge_sort(left_arr: list, right_arr: list) -> list:
    result = []
    left_idx, right_idx = 0, 0

    while left_idx < len(left_arr) and right_idx < len(right_arr):
        if left_arr[left_idx] < right_arr[right_idx]:
            result.append(left_arr[left_idx])
            left_idx += 1
        else:
            result.append(right_arr[right_idx])
            right_idx += 1

    result.extend(left_arr[left_idx:])
    result.extend(right_arr[right_idx:])

    return result


# Сортировка Шелла - это алгоритм сортировки, который улучшает обычную сортировку вставками
# Средняя сложность O(n log^2 n), Худшая сложность O(n^2)
def shell_sort(source_a: list) -> list:
    arr = [i for i in source_a]
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


# Быстрая сортировка
def quick_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left_arr = [i for i in arr if i < pivot]
    middle_arr = [i for i in arr if i == pivot]
    right_arr = [i for i in arr if i > pivot]

    return quick_sort(left_arr) + middle_arr + quick_sort(right_arr)


def main():
    ar = [1, 3, 5, 3, 7, 4, 8, 2]
    print(f'BEFORE: {ar}')

    bubble_ar = bubble_sort(ar)
    print(f'AFTER bubble_sort: {bubble_ar}')

    bi_selection_ar = bi_selection_sort(ar)
    print(f'AFTER bi_selection_sort: {bi_selection_ar}')

    selection_ar = selection_sort(ar)
    print(f'AFTER selection_sort: {selection_ar}')

    insertion_ar = insert_sort(ar)
    print(f'AFTER insert_sort: {insertion_ar}')

    merge_ar = merge_sort(ar)
    print(f'AFTER merge_sort: {merge_ar}')

    shell_ar = shell_sort(ar)
    print(f'AFTER shell_sort: {shell_ar}')

    quick_sort(ar)
    print(f'AFTER quick_sort: {ar}')

if __name__ == '__main__':
    main()
