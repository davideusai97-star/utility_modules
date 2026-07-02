'''returns true if two arrays are identical'''

def compare_arrays(file1, file2, tollerance):

    import math
    tol=tollerance         #tolerance for floating-point comparison (0.0 = exact)
    with open(file1, "r") as f1, open(file2, "r") as f2:
        for i, (line1, line2) in enumerate(zip(f1, f2), start=1):
            nums1 = [float(x) for x in line1.split()]
            nums2 = [float(x) for x in line2.split()]

            if len(nums1) != len(nums2):
                print(f"Line {i}: different number of elements")
                return False

            for j, (a, b) in enumerate(zip(nums1, nums2), start=1):
                if abs(a - b) > tol:
                    print(f"Line {i}, column {j}: {a} != {b}")
                    return False

        # Check if one file has extra lines
        extra1 = any(f1)
        extra2 = any(f2)
        if extra1 or extra2:
            print("Files have different number of lines")
            return False

    print(f"Files are equal at tolerance {tol}")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python compare_arrays.py file1 file2 tollerance")
        sys.exit(1)

    file1, file2, tollerance = sys.argv[1], sys.argv[2], sys.argv[3]
    compare_arrays(file1, file2, tollerance)