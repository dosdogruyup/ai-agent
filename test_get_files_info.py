from functions.get_files_info import get_files_info

print(
    "Result for current directory:\n",
    f"{get_files_info("calculator", ".")}\n\n",
)
print(
    "Result for 'pkg' directory:\n",
    f"{get_files_info("calculator", "pkg")}\n\n",
)
print(
    "Result for '/bin' directory:\n",
    f"{get_files_info("calculator", "/bin")}\n\n",
)
print(
    "Result for '../' directory:\n",
    f"{get_files_info("calculator", "../")}\n\n",
)
