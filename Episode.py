
import Media

def Episode(Media):

	def __init__(self, sectionType, title, naturalStartTime, naturalEndTime, duration, dayOfWeek, showSeriesTitle, episodeNumnber, seriesNumber):

		super().__init__(self, sectionType, title, naturalStartTime, naturalEndTime, duration, dayOfWeek)

		self.showSeriesTitle = showSeriesTitle
		self.episodeNumnber = episodeNumnber
		self.seriesNumber = seriesNumber
