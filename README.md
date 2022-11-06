# Subset-tuple-based-complementation-of-BA

Run using:
  ```
  python3 main.py file [optimizations]
  ```
  where:
    file: .hoa or .ba file  (when using HOA, just ... are accepted)
    optimization:  0 - optimizations turned off
                   1 - throw away states with 2colored rightmost component
                   2 - merging states
                   3 - new coloring (new color 3)
For example:
  using:
  ```
  python3 main.py input.hoa 0 1 2 3
  ```
  means that we want to complement BA saved in HOA format using all possible optimizations.
  Whereas using:
   ```
  python3 main.py input.ba 0 1 2
  ```
  means that we want to complement BA saved in BA format using just first 3 optimizations.
