# Who Pays the Bill?

A small Python program that settles the bill for a group, fairly and
with a bit of drama.

## Run it

```bash
python3 who_pays_the_bill.py
```

No extra packages needed — Python 3 only.

## How it works

1. First it asks: **split** the bill, or choose **one person** to pay?
2. Then it asks for the names (comma-separated) and the total bill.
3. **Split:** everyone pays an equal share. If the bill doesn't divide
   evenly, the leftover paise are handed out at random, so the shares
   always add up exactly to the total and no one systematically pays extra.
4. **One payer:** one name is picked at random, after a suspense pause,
   and announced as the group's hero — generosity framing, so the result
   feels good rather than resentful.

## Example

```
How do you want to handle the bill?
  1. Split it equally between everyone
  2. Choose ONE person to pay (picked at random)
Enter 1 or 2 (or type 'split' / 'one'): 1

Enter the names, separated by commas: Suhail, Aman, Priya
Enter the total bill amount: 1000

  Suhail  ₹333.34
  Aman    ₹333.33
  Priya   ₹333.33
  TOTAL   ₹1,000.00
```
