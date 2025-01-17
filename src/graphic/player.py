from manim import *
from os.path import join

class Player:  
  def __init__(self, width: float, height: float, controlsHeight: float = 0.5, targetProgress: float = 100, startProgress: float = 0, startGen: int = 0, endGen: int = 1, trackText: str = "Intro"):
    self.width = width
    self.height = height
    self.progress = startProgress / targetProgress
    self.controlsHeight = controlsHeight
    self.stop = SVGMobject(file_name = join("..", "vectors", "stop.svg"), height = self.controlsHeight*1.5).to_edge(DOWN).shift((0, self.height*3, 0))
    self.play = SVGMobject(file_name = join("..", "vectors", "play.svg"), height = self.controlsHeight*1.5).to_edge(DOWN).shift((0, self.height*3, 0))
    self.pause = SVGMobject(file_name = join("..", "vectors", "pause.svg"), height = self.controlsHeight*1.5).to_edge(DOWN).shift((0, self.height*3, 0))
    self.fastForward = SVGMobject(file_name = join("..", "vectors", "fast_forward.svg"), height = self.controlsHeight*1.5).to_corner(UR)
    self.currentButton = self.play.copy()
    self.backward = SVGMobject(file_name = join("..", "vectors", "backward.svg"), height = self.controlsHeight * 3/5).next_to(self.currentButton, LEFT, buff = MED_LARGE_BUFF).shift((0, self.height - self.controlsHeight * 3/5, 0))
    self.forward = SVGMobject(file_name = join("..", "vectors", "forward.svg"), height = self.controlsHeight * 3/5).next_to(self.currentButton, RIGHT, buff = MED_LARGE_BUFF).shift((0, self.height - self.controlsHeight * 3/5, 0))
    self.lastBuild = None
    self.animRunTime = 0.5
    self.startGen = startGen
    self.endGen = endGen
    self.targetProgress = targetProgress
    self.trackText = Text(trackText, height = self.controlsHeight, font = "Inter", weight = SEMIBOLD)

  def withProgress(self, progress: float):
    self.progress = progress / self.targetProgress
    return self
  
  def updateButton(self, targetButton: SVGMobject) -> AnimationGroup:
    return AnimationGroup(
      Transform(self.currentButton, targetButton),
      run_time = self.animRunTime
    )

  def buttonToStop(self) -> AnimationGroup:
    return self.updateButton(self.stop.copy())
    
  def buttonToPlay(self) -> AnimationGroup:
    return self.updateButton(self.play.copy())
    
  def buttonToPause(self) -> AnimationGroup:
    return self.updateButton(self.pause.copy())

  def withStopButton(self) -> AnimationGroup:
    self.currentButton = self.stop
    return self
    
  def withPlayButton(self) -> AnimationGroup:
    self.currentButton = self.play
    return self
    
  def withPauseButton(self):
    self.currentButton = self.pause
    return self
    
  def showFastForward(self) -> AnimationGroup:
    return FadeIn(self.fastForward)
  
  def withStartGen(self, startGen: int):
    self.startGen
    return self
  
  def withEndGen(self, endGen: int):
    self.endGen = endGen
    return self
  
  def toTrackText(self, txt: str) -> Animation:
    targetTxt = Text(txt, height = self.controlsHeight, font = "Inter", weight = SEMIBOLD).next_to(self.progressBarOutline, DOWN, buff = MED_SMALL_BUFF)
    a = Transform(self.trackText, targetTxt)
    self.trackText = targetTxt
    return a
  
  def buildMobj(self) -> VGroup:
    self.progressBarOutline = RoundedRectangle(corner_radius = 0.08, height = self.height, width = self.width).next_to(self.currentButton, DOWN)
    self.progressBarFill = RoundedRectangle(
      corner_radius = 0.08,
      height = self.height,
      width = self.width * (self.progress + 1e-3),
      fill_color = GRAY,
      fill_opacity = 1,
      stroke_width = 0
    ).next_to(self.currentButton, DOWN).align_to(self.progressBarOutline, LEFT)
    self.startGenText = Text(f"Gen {self.startGen}", height = self.height, font = "Inter").next_to(self.progressBarOutline, LEFT)
    self.endGenText = Text(f"Gen {self.endGen}", height = self.height, font = "Inter").next_to(self.progressBarOutline, RIGHT)
    self.trackText = self.trackText.next_to(self.progressBarOutline, DOWN, buff = MED_SMALL_BUFF)
    g =  VGroup(self.currentButton, self.backward, self.forward, self.progressBarFill, self.progressBarOutline, self.startGenText, self.endGenText, self.trackText)
    self.lastBuild = g
    return g
  
  def toProgress(self, progress: float) -> Animation:
    self.progress = progress / self.targetProgress
    return Transform(self.lastBuild, self.buildMobj())
