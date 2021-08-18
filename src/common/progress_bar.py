def print_progress_bar(message: str, step: int, total: int) -> None:
    num_digits_total = len(str(total))
    padded_step = str(step).zfill(num_digits_total)
    percent = 100 * step / total

    print(f"{message}: {padded_step}/{total} ({percent:.1f}%)", end = "\r")

    if step == total:
        print()
