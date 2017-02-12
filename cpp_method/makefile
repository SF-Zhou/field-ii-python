all: bin/beamforming

run: bin/beamforming
	bin/beamforming

bin/:
	mkdir -p bin

bin/beamforming: beamforming.cpp *.hpp method/*.hpp bin/
	g++ beamforming.cpp -o bin/beamforming -std=c++11 -O3

clean:
	rm -rf bin/
