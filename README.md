# simple_syll
Simple syllabification script.

The basic idea is that each syllable should have a vowel, and after the vowel you have to decide whether the consonant that follows should be part of the current or the next syllable.  If it's a single consonant, then have it start its own syllable.  If it's a double consonant, then have the first consonant end the current syllable, and the second consonant start the next one.

This is not perfect and may not apply in every language, but it is good enough for certain applications.  In particular it does not handle semivowels like 'y' well, which sometimes act like vowels and sometimes act like consonants.  

To use, edit the list of consonants and vowels to match your phoneset, and make 'lexfile' point to the file of words and pronunciations that you want to syllabify.  Output may be formatted in Festival syllabified lexicon format.
