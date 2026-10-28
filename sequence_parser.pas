program SequenceParser;

{$mode objfpc}{$H+}

uses
  Classes, SysUtils, fpjson, jsonparser;

type
  TEventKind = (evNoteOn, evNoteOff, evTempo, evProgram);

  TMusicEvent = record
    Kind: TEventKind;
    NoteName: string;
    DurationTicks: Integer;
  end;

  TTrack = record
    Events: array of TMusicEvent;
  end;

  TSequence = record
    SourceName: string;
    TicksPerQuarter: Integer;
    OriginalBpm: Integer;
    Tracks: array of TTrack;
  end;

function LoadSequenceFromJSON(const Filename: string): TSequence;
var
  JSONData: TJSONData;
  RootObj, RhythmObj: TJSONObject;
  RhythmArray: TJSONArray;
  I: Integer;
  Ev: TMusicEvent;
begin
  Result.SourceName := 'Unknown';
  Result.TicksPerQuarter := 480;
  Result.OriginalBpm := 120;

  JSONData := GetJSON(Filename);
  try
    if not (JSONData is TJSONObject) then
      raise Exception.Create('Root is not a JSON object');
    RootObj := TJSONObject(JSONData);
    Result.SourceName := RootObj.Get('source_game', 'Unknown');
    Result.TicksPerQuarter := RootObj.Get('ticks_per_quarter', 480);
    Result.OriginalBpm := RootObj.Get('original_bpm', 120);

    RhythmArray := RootObj.Get('extracted_rhythm', TJSONArray(nil));
    if Assigned(RhythmArray) then
    begin
      SetLength(Result.Tracks, 1);
      SetLength(Result.Tracks[0].Events, RhythmArray.Count);
      for I := 0 to RhythmArray.Count - 1 do
      begin
        RhythmObj := RhythmArray.Objects[I];
        Ev.Kind := evNoteOn;
        Ev.NoteName := RhythmObj.Get('note', 'C4');
        Ev.DurationTicks := RhythmObj.Get('duration_ticks', 480);
        Result.Tracks[0].Events[I] := Ev;
      end;
    end;
  finally
    JSONData.Free;
  end;
end;

procedure PrintSequence(const Seq: TSequence);
var
  I: Integer;
begin
  WriteLn('Source: ', Seq.SourceName);
  WriteLn('Tempo: ', Seq.OriginalBpm, ' BPM');
  WriteLn('Ticks per quarter: ', Seq.TicksPerQuarter);
  if Length(Seq.Tracks) > 0 then
  begin
    WriteLn('Events: ', Length(Seq.Tracks[0].Events));
    for I := 0 to High(Seq.Tracks[0].Events) do
    begin
      WriteLn('  #', I, ' note=', Seq.Tracks[0].Events[I].NoteName,
              ' dur=', Seq.Tracks[0].Events[I].DurationTicks);
    end;
  end;
end;

procedure ExportToCSV(const Seq: TSequence; const Filename: string);
var
  Lines: TStringList;
  I: Integer;
begin
  Lines := TStringList.Create;
  try
    Lines.Add('index,note,duration_ticks');
    if Length(Seq.Tracks) > 0 then
      for I := 0 to High(Seq.Tracks[0].Events) do
        Lines.Add(Format('%d,%s,%d',
          [I, Seq.Tracks[0].Events[I].NoteName,
           Seq.Tracks[0].Events[I].DurationTicks]));
    Lines.SaveToFile(Filename);
  finally
    Lines.Free;
  end;
end;

var
  Seq: TSequence;
begin
  WriteLn('=== Pascal Sequence Parser ===');
  if not FileExists('game_extract.json') then
  begin
    WriteLn('ERROR: game_extract.json not found.');
    Halt(1);
  end;

  Seq := LoadSequenceFromJSON('game_extract.json');
  PrintSequence(Seq);
  ExportToCSV(Seq, 'parsed_sequence.csv');
  WriteLn('Exported parsed_sequence.csv');
  WriteLn('=== Done ===');
end.
