CWD=$$(pwd)

build_image:
	docker build -t bookings_api .

dev:
	docker run --network host -w /booking_api -it --rm -v "${CWD}":/booking_api/ bookings_api bash
