from cat import Cat


cat_1 = Cat()
cat_2 = Cat()

print("猫の髭の本数")
print(cat_1.hige)
print(cat_2.hige)

cat_1.pull_out_beard()
cat_1.pull_out_beard()

print("猫の髭の本数（抜いた後）")
print(cat_1.hige)
print(cat_2.hige)

cat_1.add_beard()

for i in range(300):
    cat_2.add_beard()

print("猫の髭の本数（足した後）")
print(cat_1.hige)
print(cat_2.hige)