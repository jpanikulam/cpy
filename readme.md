CPY
==========================
CPY - America's favorite Python syntactic code generation tool.

# Why?

Code generation is annoying. Munging with AST's is more annoying. Template meta-programming is even **more** annoying. It should be easy, and you should be able to think in real syntax. Enter CPY.

For scientific computing: CPY takes advantage of intel processor features that a normally require tremendous programmer effort. It generates code that takes advantage of matrix sparsity, and is aware of its own future access pattern, enabling very agressive optimization that compilers generally can't do.

For general code generation: CPY provides tooling for programmatically producing C++ from Python. Here, the user has tremendous control, while the trivialities (like updating headers, managing headers, managing CMake, deciding when to return outputs by non-const ref, etc) are handled internally.

Often, it can help you in generating Python binding, and many packages use CPY to generate unittests.

Disclaimer: I dont't mean to knock the power of any of the tools above, like Clang's Cog, and C++'s incredible TMP power, CPY intends to solve a different, broader problem.

Under Construction. If you have a need for this, shoot me an email.

# Setup

```
sudo python setup.py develop
```

## Uninstall

```
sudo python setup.py develop --uninstall
```
