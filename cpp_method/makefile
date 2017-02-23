all: directories bin/beamforming bin/measure

directories: bin/

bin/:
	mkdir -p bin

bin/beamforming: beamforming.cpp *.hpp method/*.hpp
	g++ beamforming.cpp -o bin/beamforming -std=c++11 -O3

bin/measure: beamforming.cpp *.hpp method/*.hpp
	g++ beamforming.cpp -o bin/measure -std=c++11 -O3 -DMEASURE -march=native

clean:
	rm -rf bin/
