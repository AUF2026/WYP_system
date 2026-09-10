from wyp import solve


problem = {
    "x": "12",
    "y": "12",
}


result = solve(problem)


print("WYP? What's Your Problem?")
print("It's Deterministically Solved!")
print()
print("STRUCTURE")
print(result["structure"])
print()
print("INVARIANTS")
print(result["invariants"])
print()
print("CONSTRAINTS")
print(result["constraints"])
print()
print("QUANTITIES")
print(result["quantities"])
print()
print("MANIFESTATION")
print(result["manifestation"])
