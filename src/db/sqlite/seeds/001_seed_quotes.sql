-- ============================================================
-- SEED - QUOTES
-- ============================================================

INSERT OR IGNORE INTO quotes (
    category,
    author,
    quote,
    sort_order
)
VALUES
    ('Finance', 'Warren Buffett', 'Risk comes from not knowing what you’re doing.', 10),
    ('Finance', 'Ray Dalio', 'The biggest mistake investors make is to believe that what happened in the recent past is likely to persist.', 20),
    ('Finance', 'Benjamin Graham', 'The intelligent investor is a realist who sells to optimists and buys from pessimists.', 30),
    ('Finance', 'Charlie Munger', 'The big money is not in the buying and selling, but in the waiting.', 40),
    ('Finance', 'Peter Lynch', 'Know what you own, and know why you own it.', 50),
    ('Finance', 'John Bogle', 'The two greatest enemies of the equity fund investor are expenses and emotions.', 60),
    ('Finance', 'Paul Tudor Jones', 'Losers average losers.', 70),
    ('Finance', 'Jesse Livermore', 'Markets are never wrong, opinions often are.', 80),
    ('Finance', 'George Soros', 'It’s not whether you’re right or wrong that’s important, but how much money you make when you’re right and how much you lose when you’re wrong.', 90),
    ('Finance', 'Stanley Druckenmiller', 'I learned that nothing is foolproof. You have to be flexible.', 100),

    ('Economics', 'John Maynard Keynes', 'Markets can remain irrational longer than you can remain solvent.', 110),
    ('Economics', 'Milton Friedman', 'Inflation is always and everywhere a monetary phenomenon.', 120),
    ('Economics', 'Adam Smith', 'The real tragedy of the poor is the poverty of their aspirations.', 130),
    ('Economics', 'David Ricardo', 'The value of a commodity, therefore, depends on the relative quantity of labor which is necessary for its production.', 140),
    ('Economics', 'Joseph Schumpeter', 'Creative destruction is the essential fact about capitalism.', 150),
    ('Economics', 'Thomas Sowell', 'The first lesson of economics is scarcity: there is never enough of anything to satisfy all those who want it.', 160),
    ('Economics', 'Paul Samuelson', 'Investing should be more like watching paint dry or watching grass grow. If you want excitement, take $800 and go to Las Vegas.', 170),
    ('Economics', 'Friedrich Hayek', 'The curious task of economics is to show how little we really know.', 180);
