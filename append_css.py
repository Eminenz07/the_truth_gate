
with open(r'c:\Users\Eminence\Documents\The Truth Gate\core\static\core\css\theme.css', 'a') as f:
    with open(r'c:\Users\Eminence\Documents\The Truth Gate\core\static\core\css\mobile-overhaul.css', 'r') as src:
        f.write('\n' + src.read())
