from django.db import models


SCHACHT_KVZ = (
    ('Kabelverzweiger', 'Kabelverzweiger'),
    ('Netzverteiler', 'Netzverteiler'),
    ('Schacht', 'Schacht'),
)

EINZELROHRE = (
    ('12', '12'),
    ('24', '24'),
)

EINZELROHRTYP = (
    ('Leerrohr', 'Leerrohr'),
    ('Verbindungsrohr', 'Verbindungsrohr'),
    ('Verzweigungsrohr', 'Verzweigungsrohr'),
)

KABELTYP = (
    ('e-Fiber 2x', 'e-Fiber 2x'),
    ('LTMC', 'LTMC'),
)

KABELFARBEN = (
    ('Blau', 'Blau'),
    ('Braun', 'Braun'),
    ('Cyan', 'Cyan'),
    ('Gelb', 'Gelb'),
    ('Grau', 'Grau'),
    ('Gruen', 'Gruen'),
    ('Lila', 'Lila'),
    ('Orange', 'Orange'),
    ('Pink', 'Pink'),
    ('Rot', 'Rot'),
    ('Schwarz', 'Schwarz'),
    ('Weiss', 'Weiss'),
)

KABELLAGEN = (
    ('1', '1'),
    ('2', '2'),
)

TYPES = (
    ('PoP', 'PoP'),
    ('MFG', 'MFG'),
)

WDM = (
    ('16', '16'),
    ('32', '32'),
    ('64', '64'),
    ('128', '128'),
)


class Customer(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Cluster(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class IES(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False, unique=True)
    slots = models.IntegerField(default=0)
    linecards = models.IntegerField(default=0)
    linecard_ports = models.IntegerField(default=0)
    ports_max = models.IntegerField(default=0)
    mgmt_cards = models.IntegerField(default=0)
    mgmg_card_position_1 = models.IntegerField(default=0)
    mgmg_card_position_2 = models.IntegerField(default=0)
    mgmg_card_position_3 = models.IntegerField(default=0)
    mgmg_card_position_4 = models.IntegerField(default=0)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.ports_max = self.linecards * self.linecard_ports
        super().save(*args, **kwargs)


class RohrTyp(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    anzahl_einzelrohre = models.CharField(max_length=2, null=False, blank=False, choices=EINZELROHRE, default=EINZELROHRE[1][1])
    typ = models.CharField(max_length=20, null=False, blank=False, choices=EINZELROHRTYP, default=EINZELROHRTYP[2][1])
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class EinzelrohrTyp(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    number = models.IntegerField(default=0)
    rohr_typ = models.ForeignKey(RohrTyp, null=False, blank=False, on_delete=models.CASCADE)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rohr_typ', 'number']

    def __str__(self):
        return '{}, Rohrtyp: {}'.format(self.name, self.rohr_typ)


class Technikstandort(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, null=False, blank=False, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, null=False, blank=False, choices=TYPES, default=TYPES[0][0])
    wdm = models.CharField(max_length=10, null=False, blank=False, choices=WDM, default=WDM[2][1])
    ies_01 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_01")
    ies_02 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_02")
    ies_03 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_03")
    ies_04 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_04")
    ies_05 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_05")
    ies_06 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_06")
    ies_07 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_07")
    ies_08 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_08")
    ies_09 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_09")
    ies_10 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_10")
    ies_11 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_11")
    ies_12 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_12")
    ies_13 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_13")
    ies_14 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_14")
    ies_15 = models.ForeignKey(IES, null=True, blank=True, on_delete=models.CASCADE, related_name="ies_15")
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TechnikstandortDefault(models.Model):
    customer = models.CharField(max_length=100, null=True, blank=True)
    project = models.CharField(max_length=100, null=True, blank=True)
    cluster = models.CharField(max_length=100, null=True, blank=True)
    technikstandort_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    technikstandort_id = models.IntegerField(default=0)
    reserve_verbindungsrohr = models.IntegerField(default=0)
    reserve_verzweigungsrohr = models.IntegerField(default=0)
    fiberunit_04 = models.IntegerField(null=False, blank=False, default=0)
    fiberunit_08 = models.IntegerField(null=False, blank=False, default=0)
    fiberunit_12 = models.IntegerField(null=False, blank=False, default=0)
    fiberunit_24 = models.IntegerField(null=False, blank=False, default=0)
    fiberunit_48 = models.IntegerField(null=False, blank=False, default=0)
    reserve_tv_zentral_fiber = models.IntegerField(null=True, blank=True)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    user_updated = models.CharField(max_length=50, null=False, blank=False, default="-")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['customer', 'project', 'cluster', 'technikstandort_name']

    def __str__(self):
        return 'Grundeinstellung fuer {}'.format(self.technikstandort_name)


class Kabel(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    technikstandort = models.ForeignKey(Technikstandort, null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, null=False, blank=False, choices=KABELTYP, default=KABELTYP[1][1])
    buendel_anzahl = models.IntegerField(default=0)
    buendel_groesse = models.IntegerField(default=0)
    faser_anzahl = models.IntegerField(default=0)
    farbe = models.CharField(max_length=25, null=True, blank=True, choices=KABELFARBEN, default=KABELFARBEN[9][1])
    lagen = models.CharField(max_length=1, null=True, blank=True, choices=KABELLAGEN, default=KABELLAGEN[0][0])
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.faser_anzahl = self.buendel_anzahl * self.buendel_groesse
        super().save(*args, **kwargs)


class Rohr(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    customer = models.CharField(max_length=100, null=True, blank=True)
    project = models.CharField(max_length=100, null=True, blank=True)
    cluster = models.CharField(max_length=100, null=True, blank=True)
    technikstandort_id = models.CharField(max_length=255, null=True, blank=True)
    technikstandort = models.CharField(max_length=100, null=True, blank=True)
    schacht_kvz = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(RohrTyp, null=False, blank=False, on_delete=models.CASCADE)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Schacht_Kvz(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    customer = models.CharField(max_length=100, null=True, blank=True)
    project = models.CharField(max_length=100, null=True, blank=True)
    cluster = models.CharField(max_length=100, null=True, blank=True)
    technikstandort_id = models.CharField(max_length=255, null=True, blank=True)
    technikstandort = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=25, null=False, blank=False, choices=SCHACHT_KVZ, default=SCHACHT_KVZ[2][1])
    rohr_abgaenge = models.IntegerField(default=3)
    rohr_einzelrohre_typ = models.ForeignKey(RohrTyp, null=True, blank=True, on_delete=models.CASCADE)
    kabel_status_versorgt = models.BooleanField(default=True)
    kabel_a_seite = models.ForeignKey(Kabel, null=True, blank=True, on_delete=models.CASCADE, related_name="a_seite")
    kabel_b_seite = models.ForeignKey(Kabel, null=True, blank=True, on_delete=models.CASCADE, related_name="b_seite")
    faser_a_versorgt_von = models.IntegerField(default=0)
    faser_a_versorgt_bis = models.IntegerField(default=0)
    faser_b_versorgt_von = models.IntegerField(default=0)
    faser_b_versorgt_bis = models.IntegerField(default=0)
    geo_latitude = models.CharField(max_length=25, null=True, blank=True, default="51.165691")
    geo_longitude = models.CharField(max_length=25, null=True, blank=True, default="10.451526")
    user_created = models.CharField(max_length=50, null=False, blank=False)
    user_updated = models.CharField(max_length=50, null=False, blank=False, default="-")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def getTrueFalse(self):
        x = ['Nein' if self.kabel_status_versorgt == False else 'Ja']
        return x[0]

    def getACable(self):
        x = ['-' if self.kabel_a_seite is None else self.kabel_a_seite]
        return x[0]

    def getBCable(self):
        x = ['-' if self.kabel_b_seite is None else self.kabel_b_seite]
        return x[0]

    def getASiteFibers(self):
        x = ['-' if self.faser_a_versorgt_von == 0 or self.faser_a_versorgt_bis == 0 else '{} - {}'.format(self.faser_a_versorgt_von, self.faser_a_versorgt_bis)]
        return x[0]

    def getBSiteFibers(self):
        x = ['-' if self.faser_b_versorgt_von == 0 or self.faser_b_versorgt_bis == 0 else '{} - {}'.format(self.faser_b_versorgt_von, self.faser_b_versorgt_bis)]
        return x[0]

    def getBSite(self):
        x = ['Nein' if self.kabel_b_seite == False else 'Ja']
        return x[0]

    def status_geo(self):
        if self.geo_latitude != '51.165691' and self.geo_longitude != '10.451526':
            return 'Ja'
        else:
            return 'Nein'


class Hausanschlussrohr(models.Model):
    ort_kuerzel = models.CharField(max_length=20, null=True, blank=True)
    ort = models.CharField(max_length=50, null=True, blank=True)
    strasse = models.CharField(max_length=50, null=True, blank=True)
    ha_number = models.IntegerField(default=0, null=True, blank=True)
    ha_add = models.CharField(max_length=20, null=True, blank=True)
    we_number = models.IntegerField(default=1, null=True, blank=True)
    customer = models.CharField(max_length=100, null=True, blank=True)
    project = models.CharField(max_length=100, null=True, blank=True)
    cluster = models.CharField(max_length=100, null=True, blank=True)
    technikstandort_id = models.CharField(max_length=255, null=True, blank=True)
    technikstandort = models.CharField(max_length=100, null=True, blank=True)
    schacht_kvz = models.CharField(max_length=100, null=True, blank=True)
    rohr_typ = models.ForeignKey(RohrTyp, null=False, blank=False, on_delete=models.CASCADE)
    rohr_name = models.CharField(max_length=100, null=True, blank=True)
    einzelrohr_name = models.CharField(max_length=50, null=False, blank=False)
    einzelrohr_malfunction = models.BooleanField(default=False)
    fiberunit_size = models.CharField(max_length=10, null=True, blank=True)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    user_updated = models.CharField(max_length=50, null=False, blank=False, default="-")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['customer', 'project', 'cluster', 'technikstandort', 'schacht_kvz', 'rohr_typ']

    def __str__(self):
        return '{}_{} (Technikstandort {}, Cluster {})'.format(self.rohr_name, self.einzelrohr_name,
                                                              self.technikstandort, self.cluster)


class Wohneinheit(models.Model):
    hausanschlussrohr = models.ForeignKey(Hausanschlussrohr, null=False, blank=False, on_delete=models.CASCADE)
    we_number = models.IntegerField(null=False, blank=False, default=1)
    we_name = models.CharField(max_length=50, null=True, blank=True)
    user_created = models.CharField(max_length=50, null=False, blank=False)
    user_updated = models.CharField(max_length=50, null=False, blank=False, default="-")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wohneinheit {self.we_name}(Nr.: {self.we_number}) von {self.hausanschlussrohr}"
