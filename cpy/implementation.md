Implementation Guide
====================

This document discusses the implementation details of CPY. This is an work-in-progress, and is not guaranteed to be completed.

CPY is a tool for syntactic C++ code generation. That is, the auto-coding is done at a *syntax* level, and *not* by generating an Abstract Syntax Tree. The goal is to make it easier to create code-generation tools.

# Motivation
C++ is very verbose. Many lines perform few actions. For many things, the developer must do a lot of thinking to produce what is ultimately a deterministic result. Everything after the decision "I want to do X" should be done by a computer. Since we don't yet have general AI, we have to settle for *most* of the tedious work should be done by a computer.


# Code
There are three areas where logic takes place:

* Logic that is run at generate-time (Pure Python)

* Logic that is run at compile-time (C++ Templates)

* Logic that is run at run-time (Actual C++)

CPY enables you to use Python as your "macro language", at the same time taking care of some general trivialities associated with writing typical C++.


# Open Questions

* Should CPY provide the ability to force-insert your own code?
* Should CPY do any actual compiley activities?

# Things you SHOULD be able to do
* Make a matrix super-template, for doing CVXGEN-like matrix multiplication unrolling in arbitrary code
	* And provide an easy interface for doing so
* Automatically insert prototypes into headers
* Automatically generate CMakeLists.txt
* Do something sensible with project code stucture