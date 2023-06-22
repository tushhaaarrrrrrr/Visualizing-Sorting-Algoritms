import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


# Update the plot_bars function to use the custom color palette
def plot_bars(arr, ax):
    n = len(arr)
    custom_colors = [(0.4, 0.4, 0.4) for _ in range(n)]
    ax.clear()
    ax.bar(range(len(arr)), arr, align='edge', alpha=0.7, width=0.8, color=custom_colors)
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, int(1.1 * max(arr)))


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr


def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr


def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[i] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield arr
        yield from heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)


def partition(arr, low, high):
    i = low - 1
    pivot = arr[high]

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr
    return i + 1


def quick_sort(arr, low, high):
    if low < high:
        pi = yield from partition(arr, low, high)
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)


def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    left_arr = [0] * n1
    right_arr = [0] * n2

    for i in range(n1):
        left_arr[i] = arr[left + i]

    for j in range(n2):
        right_arr[j] = arr[mid + 1 + j]

    i = j = 0
    k = left

    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        yield arr
        k += 1

    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1
        yield arr

    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1
        yield arr


def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        yield from merge_sort(arr, left, mid)
        yield from merge_sort(arr, mid + 1, right)
        yield from merge(arr, left, mid, right)


def visualize_sorting_algorithm(sort_algorithm, algorithm_name):
    arr = random.sample(range(1, 101), 50)  # Random array of 50 elements
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title(algorithm_name)

    generator = sort_algorithm(arr)

    def update_plot(sorted_arr):
        plot_bars(sorted_arr, ax)

    anim = animation.FuncAnimation(fig, update_plot, frames=generator, interval=50, repeat=False, cache_frame_data=False)
    plt.show()


# Visualize bubble sort
visualize_sorting_algorithm(bubble_sort, "Bubble Sort")

# Visualize insertion sort
visualize_sorting_algorithm(insertion_sort, "Insertion Sort")

# Visualize heap sort
visualize_sorting_algorithm(heap_sort, "Heap Sort")

# Visualize quick sort
visualize_sorting_algorithm(lambda arr: quick_sort(arr, 0, len(arr) - 1), "Quick Sort")

# Visualize merge sort
visualize_sorting_algorithm(lambda arr: merge_sort(arr, 0, len(arr) - 1), "Merge Sort")
