# Subset-tuple-based-complementation-of-BA

Run using:
  ```
  python3 main.py file [optimizations]
  ```
  where:<br />
    file: .hoa or .ba file  (when using HOA, just ... are accepted)<br />
    optimizations:  <br />
                   0 - throw away states with 2colored rightmost component<br />
                   1 - merging states<br />
                   2 - new coloring (new color 3)<br />
For example:<br />
  using:<br />
  ```
  python3 main.py input.hoa 0 1 2
  ```
  means that we want to complement BA saved in HOA format using all possible optimizations.<br />
  Whereas using:<br />
   ```
  python3 main.py input.ba 0 1
  ```
  means that we want to complement BA saved in BA format using just first 2 optimizations.<br />
  <br />
  In case we do not want to optimise at all, run it this way (ommit optimization args):<br />
  ```
  python3 main.py file
  ```
