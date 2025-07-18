def two_sum(nums, target):
    """
    Find two numbers in the array that add up to the target.
    Returns the indices of the two numbers.
    """
    num_map = {}
    for i, num in enumerate(nums):
        if target - num in num_map:
            return [num_map[target - num], i]
        num_map[num] = i
    return None  # No solution found

# Test Cases
def test_two_sum():
    print("Testing two_sum function...")
    
    # Test Case 1: Basic case with positive numbers
    nums1 = [2, 7, 11, 15]
    target1 = 9
    result1 = two_sum(nums1, target1)
    print(f"Test 1: nums={nums1}, target={target1}")
    print(f"Result: {result1}")
    print(f"Expected: [0, 1] (nums[0] + nums[1] = 2 + 7 = 9)")
    print()
    
    # Test Case 2: Array with negative numbers
    nums2 = [3, 2, 4]
    target2 = 6
    result2 = two_sum(nums2, target2)
    print(f"Test 2: nums={nums2}, target={target2}")
    print(f"Result: {result2}")
    print(f"Expected: [1, 2] (nums[1] + nums[2] = 2 + 4 = 6)")
    print()
    
    # Test Case 3: Array with duplicate numbers
    nums3 = [3, 3]
    target3 = 6
    result3 = two_sum(nums3, target3)
    print(f"Test 3: nums={nums3}, target={target3}")
    print(f"Result: {result3}")
    print(f"Expected: [0, 1] (nums[0] + nums[1] = 3 + 3 = 6)")
    print()
    
    # Test Case 4: No solution exists
    nums4 = [1, 2, 3]
    target4 = 10
    result4 = two_sum(nums4, target4)
    print(f"Test 4: nums={nums4}, target={target4}")
    print(f"Result: {result4}")
    print(f"Expected: None (no two numbers sum to 10)")
    print()
    
    # Test Case 5: Array with negative numbers
    nums5 = [-1, -2, -3, -4, -5]
    target5 = -8
    result5 = two_sum(nums5, target5)
    print(f"Test 5: nums={nums5}, target={target5}")
    print(f"Result: {result5}")
    print(f"Expected: [2, 4] (nums[2] + nums[4] = -3 + -5 = -8)")
    print()

if __name__ == "__main__":
    test_two_sum()
