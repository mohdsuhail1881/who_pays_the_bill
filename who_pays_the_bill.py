#!/usr/bin/env python3
"""
Who Pays the Bill?
===================

A small, friendly bill-decider for friends, family and colleagues.

How it works
------------
1. First it asks ONE question: split the bill, or choose one person to pay?
2. Then it asks for the names and the total bill.
3. Split  -> everyone pays an equal share (see split_bill()).
   One    -> one name is picked at random, with a little suspense first.

The psychology behind the wording (why it feels fair, not awkward)
------------------------------------------------------------------
* Split: people accept a result more when the *process* is transparent
  and equal. So the program shows the maths, not just the answer, and
  every share is within 1 paisa of every other share.
* One payer: a random pick feels fair only if nobody can rig it, so the
  pick is made in front of everyone, after a pause. Then the result is
  framed as generosity ("today's hero") instead of a loss, which is the
  classic re-framing trick: the same outcome feels good instead of
  resentful. A compliment for the payer, and a "next time it's someone
  else's turn" line, keeps the group feeling even.
* Rounding: if the bill does not divide evenly, the leftover paise are
  handed out at random, not always to the first name, so no one is
  systematically the person who pays the extra paisa.

Run it with:  python3 who_pays_the_bill.py
No extra packages are needed — only Python's standard library.
"""

import random
import sys
import time


# ---------------------------------------------------------------------------
# Pure logic (easy to test, no input/output inside these functions)
# ---------------------------------------------------------------------------

def parse_names(text):
    """Turn 'Suhail, Aman, Priya' into ['Suhail', 'Aman', 'Priya']."""
    names = []
    for part in text.split(","):
        name = part.strip()
        if name and name not in names:
            names.append(name)
    return names


def split_bill(total, names, rng=None):
    """Split `total` equally, in paise, so the shares sum exactly to total.

    Returns a dict {name: share}. Each share differs from the exact
    equal share by less than 1 paisa, and any leftover paise go to
    randomly chosen people (not always the first name).
    """
    rng = rng or random
    if total <= 0:
        raise ValueError("Bill total must be positive.")
    if len(names) < 2:
        raise ValueError("Need at least 2 names to split a bill.")
    total_paise = round(total * 100)
    base_paise, remainder = divmod(total_paise, len(names))
    shares_paise = {name: base_paise for name in names}
    # Hand the leftover paise out at random, one paisa each.
    lucky = list(names)
    rng.shuffle(lucky)
    for name in lucky[:remainder]:
        shares_paise[name] += 1
    return {name: paise / 100 for name, paise in shares_paise.items()}


def choose_payer(names, rng=None):
    """Pick one payer at random. Raises ValueError if fewer than 2 names."""
    rng = rng or random
    if len(names) < 2:
        raise ValueError("Need at least 2 names to choose a payer.")
    return rng.choice(names)


HERO_LINES = [
    "{name} is today's hero! The rest of you: a round of applause, please.",
    "{name} steps up like a legend. Generosity looks good on you, {name}!",
    "Big respect, {name}! You just bought the whole table's happiness.",
    "{name} pays today — and earns serious bragging rights until next time.",
]


def hero_line(name, rng=None):
    rng = rng or random
    return rng.choice(HERO_LINES).format(name=name)


# ---------------------------------------------------------------------------
# Interactive helpers
# ---------------------------------------------------------------------------

def ask_choice():
    """Ask split vs one payer FIRST, as requested. Returns 'split' or 'one'."""
    while True:
        print("\nHow do you want to handle the bill?")
        print("  1. Split it equally between everyone")
        print("  2. Choose ONE person to pay (picked at random)")
        answer = input("Enter 1 or 2 (or type 'split' / 'one'): ").strip().lower()
        if answer in ("1", "split", "split it", "equal", "share"):
            return "split"
        if answer in ("2", "one", "one person", "random", "pick one"):
            return "one"
        print("Hmm, I didn't catch that. Please enter 1 for split or 2 for one payer.")


def ask_names():
    while True:
        text = input("\nEnter the names, separated by commas (e.g. Suhail, Aman, Priya): ")
        names = parse_names(text)
        if len(names) >= 2:
            return names
        print("I need at least 2 different names. Try again — commas between names.")


def ask_total():
    while True:
        text = input("Enter the total bill amount (e.g. 1250 or 1250.50): ").strip()
        # Allow a leading currency symbol, in case someone types it.
        text = text.lstrip("₹$€£").strip()
        try:
            total = float(text)
        except ValueError:
            print("That doesn't look like a number. Please enter just the amount.")
            continue
        if total <= 0:
            print("The bill has to be more than 0. What was the total?")
            continue
        return round(total, 2)


def show_split(total, names):
    shares = split_bill(total, names)
    print("\n" + "=" * 50)
    print("  FAIR AND SQUARE — SPLIT EQUALLY")
    print("=" * 50)
    print(f"Total bill: ₹{total:,.2f}  |  {len(names)} people")
    print("No awkwardness, no calculator fights. Everyone pays the same:")
    print("-" * 50)
    for name in names:
        print(f"  {name:<20} ₹{shares[name]:,.2f}")
    print("-" * 50)
    print(f"  {'TOTAL':<20} ₹{sum(shares.values()):,.2f}  (checks out exactly)")
    if len(set(shares.values())) > 1:
        print("Note: the bill didn't divide perfectly, so a few people pay")
        print("exactly 1 paisa more — chosen at random, so it's still fair.")
    print("\nEveryone walks away feeling it was equal. That's the whole trick.")
    print("=" * 50)


def show_one_payer(total, names):
    print("\nOkay… everyone close your eyes. No peeking, no fixing the result!")
    print("The pick is random, in front of everyone — that's what makes it fair.")
    for dots in ("Thinking", "Thinking.", "Thinking..", "Thinking..."):
        print(f"\r{dots}   ", end="", flush=True)
        time.sleep(0.45)
    print("\r" + " " * 20 + "\r", end="")
    print("🥁 The bill gods have spoken…\n")
    time.sleep(0.5)
    payer = choose_payer(names)
    print("=" * 50)
    print(f"  {payer} pays the full ₹{total:,.2f}!")
    print("=" * 50)
    print(hero_line(payer))
    others = [n for n in names if n != payer]
    print(f"\n{', '.join(others)}: you owe {payer} a thank-you (not money, today).")
    print("And remember: next time, the wheel turns. Today's hero was random,")
    print("so nobody can say it was rigged. That's why it stings a little less.")
    print("=" * 50)


def main():
    print("=" * 50)
    print("  🧾  WHO PAYS THE BILL?")
    print("=" * 50)
    print("The end of every awkward 'you pay, no you pay' moment.")
    print("Answer honestly, and let the program decide — fairly.")

    while True:
        mode = ask_choice()
        names = ask_names()
        total = ask_total()
        if mode == "split":
            show_split(total, names)
        else:
            show_one_payer(total, names)

        again = input("\nDo you want to run it again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\nThanks for playing! May your bills always be fair. 👋")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOkay, paused mid-bill. Run it again whenever you're ready!")
        sys.exit(0)
