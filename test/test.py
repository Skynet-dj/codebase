import curses
from time import sleep

def draw_progress_bar(stdscr):
    # Clear screen
    stdscr.clear()

    # Get screen height and width for center alignment
    height, width = stdscr.getmaxyx()

    # Set the message and bar width
    message = "Installing..."
    bar_width = 50

    # Calculate starting position for center alignment
    start_x = width // 2 - bar_width // 2
    start_y = height // 2

    # Create the progress bar
    progress = 0

    # Add a cursor off to avoid flickering
    curses.curs_set(0)

    # Show the message above the progress bar
    stdscr.addstr(start_y - 2, start_x, message, curses.A_BOLD)

    # Loop for progress bar animation
    while progress <= 100:
        # Draw the progress bar itself
        bar_filled = int(progress / 2)  # The bar width is 50, so we scale the progress by 2
        progress_bar = f"[{'#' * bar_filled}{'.' * (bar_width - bar_filled)}]"

        # Move cursor to the progress bar and print it
        stdscr.addstr(start_y, start_x, progress_bar, curses.A_REVERSE)

        # Refresh the screen to show the changes
        stdscr.refresh()

        # Sleep to simulate progress
        sleep(0.05)

        # Increment progress
        progress += 1

        # Move cursor back to the same position to overwrite the bar
        stdscr.move(start_y, start_x)

    # Wait for the user to press a key to exit
    stdscr.getch()

# Initialize curses and call the drawing function
curses.wrapper(draw_progress_bar)
