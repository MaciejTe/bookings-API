CWD=$$(pwd)

dev:
	docker run --network host -it --rm -v "${CWD}":/booking_api/ booking_api bash
