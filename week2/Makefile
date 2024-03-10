build:
    @cargo build --release

run:
    @cargo run --release -- $(filter-out $@,$(MAKECMDGOALS))

%:
    @: