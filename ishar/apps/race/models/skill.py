class RaceSkill(models.Model):
    race = models.ForeignKey(
        to=Race,
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        to=Spell,
        on_delete=models.CASCADE
    )
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'races_skills'
