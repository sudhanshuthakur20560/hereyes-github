# ⚡ DSA Solution - Two Pointers

**Pattern**: `Two Pointers`  
**Time Complexity**: $O(N)$  
**Space Complexity**: $O(1)$  

---

### 💡 Feynman Intuition
> Uses two indices converging or expanding to reduce an O(N^2) brute force nested loop down to an O(N) linear scan.

---

### 💻 Optimal C Implementation
```c
// Optimal Two Pointers (C99)
#include <stdio.h>
#include <stdbool.h>

bool twoSumSorted(const int* nums, int n, int target, int* out_i, int* out_j) {
    int left = 0, right = n - 1;
    while (left < right) {
        int current_sum = nums[left] + nums[right];
        if (current_sum == target) {
            *out_i = left;
            *out_j = right;
            return true;
        } else if (current_sum < target) {
            left++;
        } else {
            right--;
        }
    }
    return false;
}
```

---

### 🐍 Optimal Python 3 Implementation
```python
# Optimal Two Pointers (Python 3)
from typing import List, Tuple, Optional

def two_sum_sorted(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    left, right = 0, len(nums) - 1
    while left < right:
        curr_sum = nums[left] + nums[right]
        if curr_sum == target:
            return (left, right)
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return None
```

---

### 🛡️ Critical Edge Cases
- Target cannot be formed
- Array has only 2 elements
- Negative numbers and duplicates
