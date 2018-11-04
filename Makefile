CWD=$$(pwd)

build_image:
	docker build -t booking_api .

dev:
	docker run --network host -w /booking_api -it --rm -v "${CWD}":/booking_api/ booking_api bash
