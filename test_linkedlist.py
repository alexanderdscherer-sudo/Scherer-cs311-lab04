"""
Lab 4: The Memory Linker -- verification suite.

Run: python test_linkedlist.py
Prints the Success Token only if every check below passes.
"""

import base64
import hashlib
import random
import sys

from doubly_linked_list import DoublyLinkedList

ASSIGNMENT_ID = "LAB04"


def get_student_id() -> str:
    """Prompt for the student's USI username; baked into the Success Token
    so a copied/shared token decodes to someone else's name, not yours."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print(f"  ALL CHECKS PASSED -- {assignment_id}")
    print(f"  STUDENT: {student_id}")
    print("  SUCCESS TOKEN (paste this into Blackboard):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def check_pointer_consistency(dll: DoublyLinkedList, failures: list, context: str) -> bool:
    """Walk forward and backward, verifying every prev/next pointer agrees."""
    forward = []
    node = dll.head
    prev_node = None
    steps = 0
    while node is not None and steps <= len(dll) + 5:
        if node.prev is not prev_node:
            failures.append(f"{context}: node.prev mismatch during forward walk")
            return False
        forward.append(node.value)
        prev_node = node
        node = node.next
        steps += 1

    if prev_node is not dll.tail:
        failures.append(f"{context}: tail pointer does not match end of forward walk")
        return False

    backward = []
    node = dll.tail
    next_node = None
    steps = 0
    while node is not None and steps <= len(dll) + 5:
        if node.next is not next_node:
            failures.append(f"{context}: node.next mismatch during backward walk")
            return False
        backward.append(node.value)
        next_node = node
        node = node.prev
        steps += 1

    if list(reversed(backward)) != forward:
        failures.append(f"{context}: forward and backward walks disagree")
        return False

    if len(forward) != len(dll):
        failures.append(f"{context}: __len__ does not match actual node count")
        return False

    return True


def basic_correctness(failures: list) -> None:
    dll: DoublyLinkedList = DoublyLinkedList()

    dll.insert_back("A")
    dll.insert_back("B")
    dll.insert_front("Z")
    dll.insert_back("C")
    check("insert sequence produces [Z, A, B, C]", list(dll) == ["Z", "A", "B", "C"], failures)
    check_pointer_consistency(dll, failures, "after insert sequence")

    dll.delete("A")
    check("delete(A) leaves [Z, B, C]", list(dll) == ["Z", "B", "C"], failures)
    check_pointer_consistency(dll, failures, "after delete(A)")

    dll.reverse()
    check("reverse() produces [C, B, Z]", list(dll) == ["C", "B", "Z"], failures)
    check_pointer_consistency(dll, failures, "after reverse()")

    dll.insert(1, "X")
    check("insert(1, X) produces [C, X, B, Z]", list(dll) == ["C", "X", "B", "Z"], failures)
    check_pointer_consistency(dll, failures, "after insert(1, X)")

    removed = dll.delete_at(0)
    check("delete_at(0) removes head and returns it", removed == "C" and list(dll) == ["X", "B", "Z"], failures)
    check_pointer_consistency(dll, failures, "after delete_at(0)")

    empty: DoublyLinkedList = DoublyLinkedList()
    check("empty list iterates to nothing", list(empty) == [], failures)
    check("len(empty list) is 0", len(empty) == 0, failures)


def stress_test(failures: list, iterations: int = 500) -> None:
    dll: DoublyLinkedList = DoublyLinkedList()
    reference: list = []
    rng = random.Random(311)

    for i in range(iterations):
        op = rng.choice(["insert_front", "insert_back", "insert_at", "delete_at", "delete_value"])

        if op == "insert_front" or not reference:
            value = rng.randint(0, 10_000)
            dll.insert_front(value)
            reference.insert(0, value)
        elif op == "insert_back":
            value = rng.randint(0, 10_000)
            dll.insert_back(value)
            reference.append(value)
        elif op == "insert_at":
            value = rng.randint(0, 10_000)
            index = rng.randint(0, len(reference))
            dll.insert(index, value)
            reference.insert(index, value)
        elif op == "delete_at" and reference:
            index = rng.randint(0, len(reference) - 1)
            removed = dll.delete_at(index)
            expected = reference.pop(index)
            if removed != expected:
                failures.append(f"stress iteration {i}: delete_at({index}) returned {removed}, expected {expected}")
        elif op == "delete_value" and reference:
            value = rng.choice(reference)
            dll.delete(value)
            reference.remove(value)

        if list(dll) != reference:
            failures.append(f"stress iteration {i} ({op}): list content diverged from reference")
            return
        if not check_pointer_consistency(dll, failures, f"stress iteration {i} ({op})"):
            return


def main() -> int:
    failures: list = []

    print("Running basic correctness checks...\n")
    basic_correctness(failures)

    if failures:
        print(f"\n{len(failures)} check(s) failed. No token issued.")
        return 1

    print("\nRunning randomized stress test (500 operations, near head and tail)...\n")
    stress_test(failures)

    if failures:
        for f in failures[:10]:
            print(f"  [FAIL] {f}")
        print(f"\n{len(failures)} check(s) failed. No token issued.")
        return 1

    check("stress test completed with zero pointer/content divergences", True, failures)
    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
