from adventure.location import Location

locations = (
    Location('Living', (
        'This room has a couch, chairs and TV.',
        'You have entered the living room. You can watch TV here.',
        'This room has two sofas, chairs and a chandelier.',
        'A huge television that is great for watching games.'),
         (0, 'Bedroom', 'Garden', 0)),
    Location('Garden', (
        'This space has a swing, flowers and trees.',
        'You have arrived at the garden. You can exercise here',
        'This area has plants, grass and rabbits.',
        'A nice shiny bike that is fun to ride.'),
         (0,  'Kitchen',  0,  'Living')),
    Location('Kitchen', (
        'This room has a fridge, oven, and a sink.',
        'You have arrived in the kitchen. You can find food and drinks here.',
        'This living area has pizza, coke, and icecream.',
        'A red juicy fruit.'),
         ('Garden', 0, 0, 'Bedroom')),
    Location('Bedroom', ('This area has a bed, desk and a dresser.',
        'You have arrived in the bedroom. You can rest here.',
        'You see a wooden cot and a mattress on top of it.',
        'A nice, comfortable bed with pillows and sheets.'),
        ('Living', 0, 'Kitchen', 0))
)
