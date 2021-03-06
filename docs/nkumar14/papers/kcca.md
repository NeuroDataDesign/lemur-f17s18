# Kernel Canonical Correlation Analysis

### CCA

- Example case: 2 copies of a text, one in German, one in English
- We want to find projections of maximal correlation to find topics that are the same in 2 different languages
- Try maximizing correlation of projected German and English vectors
- Translates into an eigenvalue equation
- Kernel equation uses Legrange multipliers and regularization

- Presents a mathematical representation of problem, need other references for simpler solution

### Significance to Us

- It's a relevant method, but we need to look elsewhere to simplify it
- Potential open source solution [Pyrcca](http://journal.frontiersin.org/article/10.3389/fninf.2016.00049/full) with [code here](https://github.com/gallantlab/pyrcca)
