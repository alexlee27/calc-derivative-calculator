# Calculus Derivative Calculator
Link: https://calc-derivative-calculator.onrender.com/

This is a calculus [derivative](https://en.wikipedia.org/wiki/Derivative) (differentiation) calculator built with Python from **scratch** (without any math-related libraries like SymPy!) with **complete steps!**

## ⚙ How it works
To summarize, it uses [binary expression trees](https://en.wikipedia.org/wiki/Binary_expression_tree) and a lot of recursion.
### Input
- First, the program processes the plain string input into a list of "tokens".
  - For example, `'sin(x)+e^x'` is processed to `['sin', '(', 'x', ')', '+', 'e', '^', 'x']`
- The tokens are fed into the [Shunting yard algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm), and it converts the mathematical expression to a [binary expression tree](https://en.wikipedia.org/wiki/Binary_expression_tree) object.

### Differentiation
- Each tree object has a method called `differentiate`: calling it on an object returns its differentiated form.
- Differentiation rules such as the sum rule, product rule, power rule, and chain rule are coded into the program.
- For example, consider the pseudocode below for $\sin(x)$: 
```
function differentiate():
  if object = sin(x):
    return cos(x) * x.differentiate()
```
- The program also makes sure to keep track of each differentiation step to display later.

## 📚 Acknowledgements
- [This Wikipedia article](https://en.wikipedia.org/wiki/Binary_expression_tree) and [this GeeksForGeeks article](https://www.geeksforgeeks.org/program-to-convert-infix-notation-to-expression-tree/) which helped me with understanding and implementing the Shunting yard algorithm
- [Prof Liu and Prof Badr's U of T CSC110/111 notes](https://www.teach.cs.toronto.edu/~csc110y/fall/notes/) which helped me with understanding abstract syntax trees
- Stack Overflow
