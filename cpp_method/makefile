all: directories bin/beamforming bin/measure

directories: bin/

bin/:
	mkdir -p bin

bin/beamforming: beamforming.cpp *.hpp method/*.hpp
	g++-4.9 beamforming.cpp -o bin/beamforming -std=c++11 -O3 -mfpu='neon'

bin/measure: beamforming.cpp *.hpp method/*.hpp
	g++-4.9 beamforming.cpp -o bin/measure -std=c++11 -O3 -DMEASURE -march=native -mfpu='neon' -mneon-for-64bits

clean:
	rm -rf bin/
