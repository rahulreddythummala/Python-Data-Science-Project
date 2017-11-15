function GenderWords(input) 
{
  var Word;
  var MaleInformal = 0;
  var MaleFormal = 0;
  var FemaleInformal = 0;
  var FemaleFormal = 0;
  var i;

  var TextIn = input;
  var TextOutTop = "";
  var TextOutLeft = "";
  var TextOutRight = "";
  var InformalOut = "";
  var FormalOut = "";
  TextOutTop = "";
  TextOutLeft = "";
  TextOutRight = "";

  // positive=male, negative=female
  var DictionaryInformal = new Array();
  DictionaryInformal['actually']= -49;
  DictionaryInformal['am']= -42;
  DictionaryInformal['as']= 37;
  DictionaryInformal['because']= -55;
  DictionaryInformal['but']= -43;
  DictionaryInformal['ever']= 21;
  DictionaryInformal['everything']= -44;
  DictionaryInformal['good']= 31;
  DictionaryInformal['has']= -33;
  DictionaryInformal['him']= -73;
  DictionaryInformal['if']= 25;
  DictionaryInformal['in']= 10;
  DictionaryInformal['is']= 19;
  DictionaryInformal['like']= -43;
  DictionaryInformal['more']= -41;
  DictionaryInformal['now']= 33;
  DictionaryInformal['out']= -39;
  DictionaryInformal['since']= -25;
  DictionaryInformal['so']= -64;
  DictionaryInformal['some']= 58;
  DictionaryInformal['something']= 26;
  DictionaryInformal['the']= 17;
  DictionaryInformal['this']= 44;
  DictionaryInformal['too']= -38;
  DictionaryInformal['well']= 15;

  var DictionaryFormal = new Array();
  DictionaryFormal['a']= 6;
  DictionaryFormal['above']= 4;
  DictionaryFormal['and']= -4;
  DictionaryFormal['are']= 28;
  DictionaryFormal['around']= 42;
  DictionaryFormal['as']= 23;
  DictionaryFormal['at']= 6;
  DictionaryFormal['be']= -17;
  DictionaryFormal['below']= 8;
  DictionaryFormal['her']= -9;
  DictionaryFormal['hers']= -3;
  DictionaryFormal['if']= -47;
  DictionaryFormal['is']= 8;
  DictionaryFormal['it']= 6;
  DictionaryFormal['many']= 6;
  DictionaryFormal['me']= -4;
  DictionaryFormal['more']= 34;
  DictionaryFormal['myself']= -4;
  DictionaryFormal['not']= -27;
  DictionaryFormal['said']= 5;
  DictionaryFormal['she']= -6;
  DictionaryFormal['should']= -7;
  DictionaryFormal['the']= 7;
  DictionaryFormal['these']= 8;
  DictionaryFormal['to']= 2;
  DictionaryFormal['was']= -1;
  DictionaryFormal['we']= -8;
  DictionaryFormal['what']= 35;
  DictionaryFormal['when']= -17;
  DictionaryFormal['where']= -18;
  DictionaryFormal['who']= 19;
  DictionaryFormal['with']= -52;
  DictionaryFormal['your']= -17;

  // Normalize all of the words
  Word = TextIn.toLowerCase();
  // Create an array containing all of the different words.
  var TextArray = Word.split(/[^a-zA-Z]+/);
  if (TextArray[TextArray.length-1] == "") { TextArray.length--; }
  TextOutTop += "Total words: " + TextArray.length + "\n";
  if (TextArray.length < 300)
    {
    TextOutTop += "Too few words.  Try 300 words or more.";
    }

  // For each word, add up the values from the dictionary.
  // If the word is not in the dictionary, then ignore it.
  for(i=0; i < TextArray.length; i++)
	{
	Word = TextArray[i];
	if (!isNaN(DictionaryInformal[Word]))
		{
		if (DictionaryInformal[Word] > 0)
			{ MaleInformal += DictionaryInformal[Word]; }
		if (DictionaryInformal[Word] < 0)
			{ FemaleInformal -= DictionaryInformal[Word]; }
		}
	if (!isNaN(DictionaryFormal[Word]))
		{
		if (DictionaryFormal[Word] > 0)
			{ MaleFormal += DictionaryFormal[Word]; }
		if (DictionaryFormal[Word] < 0)
			{ FemaleFormal -= DictionaryFormal[Word]; }
		}
	}

  // Display results
  var Percent;
  var Weak=0;

  TextOutLeft += "Genre: Informal\n";
  TextOutLeft += "  Female = " + FemaleInformal + "\n";
  TextOutLeft += "  Male   = " + MaleInformal + "\n";
  if (MaleInformal + FemaleInformal > 0)
    { Percent = MaleInformal * 100.0 / (MaleInformal + FemaleInformal); }
  else { Percent=0; }
  Percent *= 100;
  Percent = parseInt(Percent) / 100.0;
  TextOutLeft += "  Difference = " + (MaleInformal-FemaleInformal) + "; " + Percent + "%\n";
  TextOutLeft += "  Verdict: ";
  if ((Percent > 40) && (Percent < 60)) { Weak++; TextOutLeft += "Weak "; }
  if (MaleInformal > FemaleInformal) { TextOutLeft += "MALE"; InformalOut = "MALE"; }
  else if (MaleInformal < FemaleInformal) { TextOutLeft += "FEMALE"; InformalOut = "FEMALE"; }
  else { TextOutLeft += "unknown"; InformalOut = "unkown"; }
  if (Weak > 0)
    { TextOutLeft += "\n\nWeak emphasis could indicate European."; }

  Weak=0;
  TextOutRight += "Genre: Formal\n";
  TextOutRight += "  Female = " + FemaleFormal + "\n";
  TextOutRight += "  Male   = " + MaleFormal + "\n";
  if (MaleFormal + FemaleFormal > 0)
    { Percent = MaleFormal * 100.0 / (MaleFormal + FemaleFormal); }
  else { Percent=0.001; }
  Percent *= 100;
  Percent = parseInt(Percent) / 100.0;
  TextOutRight += "  Difference = " + (MaleFormal-FemaleFormal) + "; " + Percent + "%\n";
  TextOutRight += "  Verdict: ";
  if ((Percent > 40) && (Percent < 60)) { Weak++; TextOutRight += "Weak "; }
  if (MaleFormal > FemaleFormal) { TextOutRight += "MALE"; FormalOut = "MALE"; }
  else if (MaleFormal < FemaleFormal) { TextOutRight += "FEMALE"; FormalOut = "FEMALE"; }
  else { TextOutRight += "unknown"; FormalOut = "unknown"; }
  if (Weak > 0)
    { TextOutRight += "\n\nWeak emphasis could indicate European."; }
  return [TextOutLeft, TextOutRight, TextOutTop, ["Informal", InformalOut], ["Formal", FormalOut]];
}

function ClearForm(form)
{
    form.Text.value = "";
    form.ResultsTop.value = "";
    form.ResultsLeft.value = "";
    form.ResultsRight.value = "";
}

function Test()
{
  return "success";
}

Test();