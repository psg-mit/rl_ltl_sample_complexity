Install Docker


```bash
docker build -t rl_ltl_pac .
```

The docker image build takes around 15 mins on a 12-core CPU machine.


```bash
docker run -it -p 8081:8081 --rm rl_ltl_pac
```

Make sure 8081 is unoccupied, or you can tweak 8081 to an unoccupied port
